from typing import List, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from app.models import MessageSenderType


class ChatRequest(BaseModel):
    customer_id: str
    message: str
    channel: Optional[str] = "web"


class MessageRead(BaseModel):
    id: UUID
    sender_type: MessageSenderType
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    conversation_id: UUID
    reply: str
    intent: str
    sentiment: str
    tags: List[str]
    confidence: float
    messages: List[MessageRead]
