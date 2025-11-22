"""initial schema

Revision ID: 2025_01_01_000001
Revises:
Create Date: 2025-01-01 00:00:01.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "2025_01_01_000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role = postgresql.ENUM("admin", "agent", name="user_role")
    user_role.create(op.get_bind(), checkfirst=True)

    conversation_status = postgresql.ENUM(
        "open", "assigned", "resolved", name="conversation_status"
    )
    conversation_status.create(op.get_bind(), checkfirst=True)

    message_sender_type = postgresql.ENUM(
        "customer", "agent", "ai", "system", name="message_sender_type"
    )
    message_sender_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", sa.String(length=255), nullable=True),
        sa.Column("channel", sa.String(length=50), nullable=False, server_default="web"),
        sa.Column("status", conversation_status, nullable=False),
        sa.Column("last_intent", sa.String(length=50), nullable=True),
        sa.Column("last_sentiment", sa.String(length=50), nullable=True),
        sa.Column("last_confidence", sa.String(length=32), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column("assigned_agent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["assigned_agent_id"], ["users.id"], ondelete="SET NULL"),
    )

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sender_type", message_sender_type, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.execute("DROP TYPE IF EXISTS message_sender_type CASCADE")
    op.execute("DROP TYPE IF EXISTS conversation_status CASCADE")
    op.execute("DROP TYPE IF EXISTS user_role CASCADE")
