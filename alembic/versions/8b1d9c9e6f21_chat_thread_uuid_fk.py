"""align chat thread reference with thread uuid

Revision ID: 8b1d9c9e6f21
Revises: 4469d970f4b3
Create Date: 2026-08-03 17:50:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8b1d9c9e6f21"
down_revision: Union[str, Sequence[str], None] = "4469d970f4b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "chats",
        sa.Column("thread_uuid", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.execute(
        """
        UPDATE chats
        SET thread_uuid = threads.thread_id
        FROM threads
        WHERE chats.thread_id = threads.id
        """
    )

    op.drop_constraint("chats_thread_id_fkey", "chats", type_="foreignkey")
    op.drop_column("chats", "thread_id")
    op.alter_column("chats", "thread_uuid", new_column_name="thread_id")
    op.alter_column("chats", "thread_id", nullable=False)
    op.create_foreign_key(
        "chats_thread_id_fkey",
        "chats",
        "threads",
        ["thread_id"],
        ["thread_id"],
        ondelete="CASCADE",
    )
    op.create_index("ix_chats_thread_id", "chats", ["thread_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_chats_thread_id", table_name="chats")
    op.drop_constraint("chats_thread_id_fkey", "chats", type_="foreignkey")

    op.add_column(
        "chats",
        sa.Column("thread_old_id", sa.Integer(), nullable=True),
    )

    op.execute(
        """
        UPDATE chats
        SET thread_old_id = threads.id
        FROM threads
        WHERE chats.thread_id = threads.thread_id
        """
    )

    op.drop_column("chats", "thread_id")
    op.alter_column("chats", "thread_old_id", new_column_name="thread_id")
    op.alter_column("chats", "thread_id", nullable=False)
    op.create_foreign_key(
        "chats_thread_id_fkey",
        "chats",
        "threads",
        ["thread_id"],
        ["id"],
        ondelete="CASCADE",
    )
