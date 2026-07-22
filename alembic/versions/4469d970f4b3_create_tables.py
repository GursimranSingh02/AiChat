"""create tables

Revision ID: 4469d970f4b3
Revises: 
Create Date: 2026-07-22 12:40:08.617358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '4469d970f4b3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create enum type first
    user_role = postgresql.ENUM('ADMIN', 'USER', name='userrole')
    user_role.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('role', postgresql.ENUM('ADMIN', 'USER', name='userrole', create_type=False), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_members_email'), 'members', ['email'], unique=True)
    op.create_index(op.f('ix_members_id'), 'members', ['id'], unique=False)

    op.create_table(
        'threads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('thread_name', sa.String(length=255), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['members.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_threads_id'), 'threads', ['id'], unique=False)
    op.create_index(op.f('ix_threads_thread_id'), 'threads', ['thread_id'], unique=True)

    op.create_table(
        'chats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_query', sa.Text(), nullable=False),
        sa.Column('llm_response', sa.Text(), nullable=False),
        sa.Column('meta_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('thread_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_id'), 'chats', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_chats_id'), table_name='chats')
    op.drop_table('chats')
    
    op.drop_index(op.f('ix_threads_thread_id'), table_name='threads')
    op.drop_index(op.f('ix_threads_id'), table_name='threads')
    op.drop_table('threads')
    
    op.drop_index(op.f('ix_members_id'), table_name='members')
    op.drop_index(op.f('ix_members_email'), table_name='members')
    op.drop_table('members')
    
    # Drop enum type
    user_role = postgresql.ENUM('ADMIN', 'USER', name='userrole')
    user_role.drop(op.get_bind(), checkfirst=True)
