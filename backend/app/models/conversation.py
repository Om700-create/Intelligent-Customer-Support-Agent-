import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as PgEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class ConversationStatus(str, Enum):
    open = "open"
    assigned = "assigned"
    resolved = "resolved"


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String(255), nullable=True, index=True)
    channel = Column(String(50), nullable=False, default="web")
    status = Column(PgEnum(ConversationStatus, name="conversation_status"), nullable=False, default=ConversationStatus.open)

    last_intent = Column(String(50), nullable=True)
    last_sentiment = Column(String(50), nullable=True)
    last_confidence = Column(String(32), nullable=True)
    tags = Column(Text, nullable=True)

    assigned_agent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    assigned_agent = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message",
        back_populates="conversation",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
