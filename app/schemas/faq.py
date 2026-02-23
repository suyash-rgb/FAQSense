from pydantic import BaseModel
from typing import Optional

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase):
    id: int

    class Config:
        from_attributes = True

class FAQAskRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None

class FAQAskResponse(BaseModel):
    answer: str
