from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core_deps import get_current_admin
from app.models import Conversation, Message, User, UserRole
from app.schemas.admin import (
    ConversationSummary,
    ConversationDetail,
    MessageRead,
    ConversationUpdate,
    AgentRead,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/conversations", response_model=List[ConversationSummary])
def list_conversations(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    convos = db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    return [ConversationSummary.model_validate(c) for c in convos]


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(conversation_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    convo = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == convo.id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return ConversationDetail(
        conversation=ConversationSummary.model_validate(convo),
        messages=[MessageRead.model_validate(m) for m in msgs],
    )


@router.patch("/conversations/{conversation_id}", response_model=ConversationSummary)
def update_conversation(
    conversation_id: UUID,
    update: ConversationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    convo = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if update.status is not None:
        convo.status = update.status
    if update.assigned_agent_id is not None:
        agent = db.query(User).filter(User.id == update.assigned_agent_id).first()
        if not agent or agent.role not in (UserRole.agent, UserRole.admin):
            raise HTTPException(status_code=400, detail="Invalid agent")
        convo.assigned_agent_id = update.assigned_agent_id

    db.commit()
    db.refresh(convo)
    return ConversationSummary.model_validate(convo)


@router.get("/agents", response_model=List[AgentRead])
def list_agents(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    agents = (
        db.query(User)
        .filter(User.role.in_([UserRole.agent, UserRole.admin]))
        .order_by(User.full_name.asc())
        .all()
    )
    return [AgentRead.model_validate(a) for a in agents]
