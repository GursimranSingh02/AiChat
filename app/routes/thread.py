from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.member import Member
from app.schema.response.thread import (
    ThreadListItem,
    ThreadListResponse,
    ThreadListResponseData,
)
from app.services.thread_service import ThreadService

router = APIRouter(prefix="/threads", tags=["threads"])
thread_service = ThreadService()


@router.get("", response_model=ThreadListResponse)
def list_threads(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Member = Depends(get_current_user),
):
    threads, total = thread_service.list_user_threads(
        db,
        user_id=current_user.id,
        page=page,
        limit=limit,
    )

    thread_items = [
        ThreadListItem(thread_id=thread.thread_id, thread_name=thread.thread_name)
        for thread in threads
    ]

    return ThreadListResponse(
        status=200,
        message="Threads fetched successfully",
        data=ThreadListResponseData(
            threads=thread_items,
            page=page,
            limit=limit,
            total=total,
            total_pages=thread_service.total_pages(total, limit),
        ),
    )
