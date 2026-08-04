from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.member import Member
from app.schema.request.chat import ChatRequest
from app.schema.response.chat import ChatResponse, ChatResponseData
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user),
):
    try:
        thread = chat_service.get_or_create_thread(
            db,
            user_id=current_user.id,
            query=payload.query,
            thread_id=payload.thread_id,
        )

        response = chat_service.generate_response(
            db,
            query=payload.query,
            thread_uuid=thread.thread_id,
        )

        chat_service.persist_chat(
            db,
            thread=thread,
            query=payload.query,
            response=response,
        )
        db.commit()
        db.refresh(thread)

        return ChatResponse(
            status=200,
            message="Chat response generated successfully",
            data=ChatResponseData(
                thread_id=thread.thread_id,
                thread_name=thread.thread_name,
                query=payload.query.strip(),
                response=response,
            ),
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except PermissionError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )
    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process chat request",
        )
