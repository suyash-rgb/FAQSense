from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FAQAnalyticResponse(BaseModel):
    original_question: str
    hit_count: int
    last_hit_at: datetime

    class Config:
        from_attributes = True

class ChatbotStatsResponse(BaseModel):
    total_faq_hits: int
    total_enquiries: int
    total_conversations: int
    resolved_enquiries: int
    total_chatbot_clicks: int
    top_faqs: List[FAQAnalyticResponse]
