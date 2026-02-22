from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    sender: str  # "visitor" or "bot"
    content: str

class MessageCreate(MessageBase):
    conversation_id: int

class MessageResponse(MessageBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ConversationBase(BaseModel):
    chatbot_id: int
    visitor_id: str

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    started_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)
