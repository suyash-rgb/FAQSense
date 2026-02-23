from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from app.schemas.conversation import ConversationCreate, ConversationResponse, MessageResponse
from app.services import conversation_service
from typing import List

router = APIRouter()

@router.post("/", response_model=ConversationResponse, status_code=201)
async def create_conversation(conv_in: ConversationCreate):
    try:
        return conversation_service.start_conversation(db.session, conv_in.chatbot_id, conv_in.visitor_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    conversation = conversation_service.get_conversation(db.session, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # SQLAlchemy will automatically load messages if relationship is configured correctly
    return conversation

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    return conversation_service.get_conversation_history(db.session, conversation_id)
