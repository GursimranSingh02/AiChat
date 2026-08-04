from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.member import Member
from app.schema.response.thread_conversation import (
    ThreadConversationItem,
    ThreadConversationResponse,
    ThreadConversationResponseData,
)
from app.services.thread_service import ThreadService

router = APIRouter(prefix="/thread", tags=["thread-conversation"])
thread_service = ThreadService()


@router.get("/{thread_id}", response_model=ThreadConversationResponse)
def get_thread_conversation(
    thread_id: UUID,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user),
):
    thread = thread_service.get_user_thread_conversation(
        db,
        user_id=current_user.id,
        thread_id=thread_id,
    )

    if thread is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thread not found",
        )

    chats = thread_service.list_thread_messages(db, thread_id=thread_id)
    messages = [
        ThreadConversationItem(
            query=chat.user_query,
            response=chat.llm_response,
        )
        for chat in chats
    ]

    return ThreadConversationResponse(
        status=200,
        message="Thread conversation fetched successfully",
        data=ThreadConversationResponseData(
            thread_id=thread.thread_id,
            thread_name=thread.thread_name,
            messages=messages,
        ),
    )
