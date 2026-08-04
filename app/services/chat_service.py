import logging
from uuid import UUID, uuid4

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat import Chat
from app.models.thread import Thread
from app.prompts.chat import chat_prompt
from app.safety import validate_query


class ChatService:
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=settings.GOOGLE_API_KEY,
            client_args={"trust_env": False},
        )
        self.parser = StrOutputParser()
        self.chain = chat_prompt | self.llm | self.parser

    def _get_history_messages(self, db: Session, thread_uuid: UUID):
        history_messages = []
        recent_chats = (
            db.query(Chat)
            .filter(Chat.thread_id == thread_uuid)
            .order_by(Chat.created_at.desc(), Chat.id.desc())
            .limit(settings.ACCESS_PAST_MESSAGES_COUNT)
            .all()
        )

        for chat in reversed(recent_chats):
            history_messages.append(HumanMessage(content=chat.user_query))
            history_messages.append(AIMessage(content=chat.llm_response))

        return history_messages

    def _thread_name_from_query(self, query: str) -> str:
        cleaned = (query or "").strip()
        return cleaned[:5] or "thread"

    def get_or_create_thread(
        self,
        db: Session,
        *,
        user_id: int,
        query: str,
        thread_id: UUID | None = None,
    ) -> Thread:
        thread_uuid = thread_id or uuid4()

        thread = db.query(Thread).filter(Thread.thread_id == thread_uuid).first()
        if thread:
            if thread.user_id != user_id:
                raise PermissionError("Thread does not belong to the current user")
            return thread

        thread = Thread(
            thread_id=thread_uuid,
            thread_name=self._thread_name_from_query(query),
            user_id=user_id,
        )
        db.add(thread)
        db.flush()
        return thread

    def generate_response(self, db: Session, *, query: str, thread_uuid: UUID) -> str:
        is_valid, message = validate_query(query)
        if not is_valid:
            raise ValueError(message)

        history = self._get_history_messages(db, thread_uuid)

        try:
            return self.chain.invoke(
                {
                    "history": history,
                    "question": query.strip(),
                }
            )
        except Exception as exc:
            logging.exception("Failed to generate chat response")
            error_text = str(exc).lower()

            if "connecterror" in error_text or "actively refused" in error_text:
                raise RuntimeError(
                    "I could not reach the Gemini API from this environment."
                ) from exc

            if "not_found" in error_text or "no longer available" in error_text:
                raise RuntimeError(
                    "The configured Gemini model is not available."
                ) from exc

            if (
                "api key" in error_text
                or "unauthorized" in error_text
                or "forbidden" in error_text
            ):
                raise RuntimeError(
                    "The Gemini API rejected the request. Check GOOGLE_API_KEY."
                ) from exc

            raise RuntimeError(
                "Sorry, something went wrong while generating the response."
            ) from exc

    def persist_chat(
        self,
        db: Session,
        *,
        thread: Thread,
        query: str,
        response: str,
    ) -> Chat:
        chat = Chat(
            user_query=query.strip(),
            llm_response=response,
            thread_id=thread.thread_id,
        )
        db.add(chat)
        db.flush()
        return chat
