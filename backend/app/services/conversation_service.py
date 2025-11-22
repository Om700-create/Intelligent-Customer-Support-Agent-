from sqlalchemy.orm import Session

from app.models import (
    Conversation,
    ConversationStatus,
    Message,
    MessageSenderType,
)
from app.services.huggingface_textgen import HFTextGenService
from app.services.huggingface_classifier import HFClassifierService
from app.prompts.system_prompt_loader import get_system_prompt


class ConversationService:
    def __init__(self, db: Session):
        self.db = db
        self.textgen = HFTextGenService()
        self.classifier = HFClassifierService()

    def get_or_create_conversation(self, customer_id: str, channel="web") -> Conversation:
        convo = (
            self.db.query(Conversation)
            .filter_by(customer_id=customer_id, status=ConversationStatus.open)
            .first()
        )
        if convo:
            return convo

        convo = Conversation(
            customer_id=customer_id,
            channel=channel,
            status=ConversationStatus.open,
        )
        self.db.add(convo)
        self.db.commit()
        self.db.refresh(convo)
        return convo

    def save_message(self, conversation_id, sender: MessageSenderType, content: str) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            sender_type=sender,
            content=content,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    async def process_message(self, customer_id: str, text: str, channel: str = "web"):
        convo = self.get_or_create_conversation(customer_id, channel=channel)

        self.save_message(convo.id, MessageSenderType.customer, text)

        intent, intent_conf = await self.classifier.classify_intent(text)
        sentiment = await self.classifier.classify_sentiment(text)
        tag, tag_conf = await self.classifier.classify_tags(text)

        convo.last_intent = intent
        convo.last_sentiment = sentiment
        convo.last_confidence = str(round(intent_conf, 3))
        current_tags = (convo.tags or "").split(",") if convo.tags else []
        if tag not in current_tags:
            current_tags.append(tag)
        convo.tags = ",".join([t for t in current_tags if t])
        self.db.commit()
        self.db.refresh(convo)

        system_prompt = get_system_prompt()

        final_prompt = f"{system_prompt}\n\nConversation so far:\n"

        messages = (
            self.db.query(Message)
            .filter_by(conversation_id=convo.id)
            .order_by(Message.created_at.asc())
            .all()
        )

        for msg in messages:
            prefix = {
                MessageSenderType.customer: "[USER]",
                MessageSenderType.agent: "[AGENT]",
                MessageSenderType.ai: "[AI]",
                MessageSenderType.system: "[SYSTEM]",
            }[msg.sender_type]
            final_prompt += f"{prefix} {msg.content}\n"

        final_prompt += "[AI]:"

        ai_reply = await self.textgen.generate(final_prompt)

        self.save_message(convo.id, MessageSenderType.ai, ai_reply)

        return convo, ai_reply, intent, sentiment, convo.tags.split(","), intent_conf
