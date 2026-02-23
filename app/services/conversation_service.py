from sqlalchemy.orm import Session
from app.models.platform import Conversation, Message, Visitor
from app.schemas.conversation import ConversationCreate, MessageCreate
from typing import List, Optional
import uuid

def get_or_create_visitor(db: Session, visitor_id: str) -> Visitor:
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    if not visitor:
        visitor = Visitor(id=visitor_id)
        db.add(visitor)
        db.commit()
        db.refresh(visitor)
    return visitor

def start_conversation(db: Session, chatbot_id: int, visitor_id: str) -> Conversation:
    # Ensure visitor exists
    get_or_create_visitor(db, visitor_id)
    
    db_conversation = Conversation(
        chatbot_id=chatbot_id,
        visitor_id=visitor_id
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_session_conversation(db: Session, chatbot_id: int, session_id: str) -> Conversation:
    """
    Finds or creates a conversation record for a given session string.
    This allows the frontend to pass a random string and we manage the DB ID internally.
    """
    # Try to find an existing conversation for this session (visitor_id) and chatbot
    # Note: In a real app, you might want to expire sessions or have more complex mapping.
    conversation = db.query(Conversation).filter(
        Conversation.chatbot_id == chatbot_id,
        Conversation.visitor_id == session_id
    ).first()
    
    if not conversation:
        conversation = start_conversation(db, chatbot_id, session_id)
        
    return conversation

def log_message(db: Session, conversation_id: str, sender: str, content: str) -> Message:
    db_message = Message(
        conversation_id=conversation_id,
        sender=sender,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation(db: Session, conversation_id: str) -> Optional[Conversation]:
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_conversation_history(db: Session, conversation_id: str) -> List[Message]:
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()

def get_user_conversations(db: Session, user_id: str) -> List[Conversation]:
    # This might be needed for the dashboard later
    # Joining with Chatbot to filter by user_id
    from app.models.platform import Chatbot
    return db.query(Conversation).join(Chatbot).filter(Chatbot.user_id == user_id).all()
