from sqlalchemy.orm import Session
from app.models.platform import FAQAnalytics
from datetime import datetime
from typing import List

def record_faq_hit(db: Session, chatbot_id: int, question_text: str):
    """
    Increment hit count for an original FAQ question.
    """
    analytics = db.query(FAQAnalytics).filter(
        FAQAnalytics.chatbot_id == chatbot_id,
        FAQAnalytics.original_question == question_text
    ).first()
    
    if analytics:
        analytics.hit_count += 1
        analytics.last_hit_at = datetime.utcnow()
    else:
        analytics = FAQAnalytics(
            chatbot_id=chatbot_id,
            original_question=question_text,
            hit_count=1,
            last_hit_at=datetime.utcnow()
        )
        db.add(analytics)
    
    db.commit()

def get_top_faqs(db: Session, chatbot_id: int, limit: int = 5) -> List[str]:
    """
    Get the most frequently asked questions for a chatbot.
    """
    results = db.query(FAQAnalytics).filter(
        FAQAnalytics.chatbot_id == chatbot_id
    ).order_by(FAQAnalytics.hit_count.desc()).limit(limit).all()
    
    return [r.original_question for r in results]
