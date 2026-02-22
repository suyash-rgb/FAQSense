from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ChatbotBase(BaseModel):
    name: str
    is_active: bool = True

class ChatbotCreate(ChatbotBase):
    pass

class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class ChatbotResponse(ChatbotBase):
    id: int
    user_id: str
    csv_file_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
