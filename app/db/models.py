import enum
import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    func,
)

from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(enum.Enum):
    ADMIN = "Admin"
    USER = "User"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    is_active = Column(Boolean, default=True)

    last_login = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    threads = relationship(
        "Thread",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)

    thread_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    thread_name = Column(String(255), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="CASCADE"),
        nullable=False,
    )

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship("Member", back_populates="threads")

    chats = relationship(
        "Chat",
        back_populates="thread",
        cascade="all, delete-orphan",
    )


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    user_query = Column(Text, nullable=False)

    llm_response = Column(Text, nullable=False)

    meta_data = Column(JSONB, nullable=True)

    thread_id = Column(
        Integer,
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    thread = relationship("Thread", back_populates="chats")