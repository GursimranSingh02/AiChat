from math import ceil

from sqlalchemy.orm import Session

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
