from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models import ConversationStatus, MessageSenderType, UserRole


class ConversationSummary(BaseModel):
    id: UUID
    customer_id: Optional[str]
    channel: str
    status: ConversationStatus
    last_intent: Optional[str]
    last_sentiment: Optional[str]
    last_confidence: Optional[str]
    tags: Optional[str]
    assigned_agent_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageRead(BaseModel):
    id: UUID
    sender_type: MessageSenderType
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationDetail(BaseModel):
    conversation: ConversationSummary
    messages: List[MessageRead]


class ConversationUpdate(BaseModel):
    status: Optional[ConversationStatus] = None
    assigned_agent_id: Optional[UUID] = None


class AgentRead(BaseModel):
    id: UUID
    full_name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True
