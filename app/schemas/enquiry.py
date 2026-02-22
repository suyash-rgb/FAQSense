from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EnquiryBase(BaseModel):
    query_text: str
    visitor_name: str
    visitor_email: Optional[EmailStr] = None
    visitor_phone: Optional[str] = None

class EnquiryCreate(EnquiryBase):
    pass

class EnquiryUpdate(BaseModel):
    status: Optional[str] = None # "open", "resolved"
    admin_notes: Optional[str] = None

class EnquiryResponse(EnquiryBase):
    id: int
    chatbot_id: int
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
