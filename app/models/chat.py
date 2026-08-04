import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(Text, nullable=False)
    llm_response = Column(Text, nullable=False)
    meta_data = Column(JSONB, nullable=True)
    thread_id = Column(
        UUID(as_uuid=True),
        ForeignKey("threads.thread_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    thread = relationship("Thread", back_populates="chats")
