from math import ceil
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.chat import Chat
from app.models.thread import Thread


class ThreadService:
    def list_user_threads(
        self,
        db: Session,
        *,
        user_id: int,
        page: int,
        limit: int,
    ) -> tuple[list[Thread], int]:
        query = (
            db.query(Thread)
            .filter(
                Thread.user_id == user_id,
                Thread.is_deleted.is_(False),
            )
        )

        total = query.count()
        threads = (
            query.order_by(Thread.created_at.desc(), Thread.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return threads, total

    @staticmethod
    def total_pages(total: int, limit: int) -> int:
        return ceil(total / limit) if total else 0

    def get_user_thread_conversation(
        self,
        db: Session,
        *,
        user_id: int,
        thread_id: UUID,
    ) -> Thread | None:
        return (
            db.query(Thread)
            .filter(
                Thread.thread_id == thread_id,
                Thread.user_id == user_id,
                Thread.is_deleted.is_(False),
            )
            .first()
        )

    def list_thread_messages(
        self,
        db: Session,
        *,
        thread_id: UUID,
    ) -> list[Chat]:
        return (
            db.query(Chat)
            .filter(Chat.thread_id == thread_id)
            .order_by(Chat.created_at.asc(), Chat.id.asc())
            .all()
        )
