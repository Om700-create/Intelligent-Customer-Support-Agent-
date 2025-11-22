from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, MessageRead
from app.services.conversation_service import ConversationService
from app.models import Message

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def chat_message(req: ChatRequest, db: Session = Depends(get_db)):
    if not req.customer_id:
        raise HTTPException(status_code=400, detail="customer_id is required")

    service = ConversationService(db)
    convo, reply, intent, sentiment, tags, conf = await service.process_message(
        customer_id=req.customer_id,
        text=req.message,
        channel=req.channel or "web",
    )

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == convo.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    messages_out = [MessageRead.model_validate(m) for m in messages]

    return ChatResponse(
        conversation_id=convo.id,
        reply=reply,
        intent=intent,
        sentiment=sentiment,
        tags=tags,
        confidence=conf,
        messages=messages_out,
    )
