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

def get_top_faqs(db: Session, chatbot_id: int, limit: int = 5) -> List[FAQAnalytics]:
    """
    Get the most frequently asked questions for a chatbot.
    """
    return db.query(FAQAnalytics).filter(
        FAQAnalytics.chatbot_id == chatbot_id
    ).order_by(FAQAnalytics.hit_count.desc()).limit(limit).all()

def get_chatbot_stats(db: Session, chatbot_id: int):
    """
    Get aggregated stats for the chatbot dashboard.
    """
    from app.models.platform import Enquiry, Conversation, FAQAnalytics
    from sqlalchemy import func

    # Total hits across all FAQs
    total_hits = db.query(func.sum(FAQAnalytics.hit_count)).filter(
        FAQAnalytics.chatbot_id == chatbot_id
    ).scalar() or 0

    # Total enquiries
    total_enquiries = db.query(Enquiry).filter(
        Enquiry.chatbot_id == chatbot_id
    ).count()

    # Resolved enquiries
    resolved_enquiries = db.query(Enquiry).filter(
        Enquiry.chatbot_id == chatbot_id,
        Enquiry.status == "resolved"
    ).count()

    # Total conversations
    total_conversations = db.query(Conversation).filter(
        Conversation.chatbot_id == chatbot_id
    ).count()

    # Top FAQs
    top_faqs = get_top_faqs(db, chatbot_id, limit=5)

    return {
        "total_faq_hits": total_hits,
        "total_enquiries": total_enquiries,
        "total_conversations": total_conversations,
        "resolved_enquiries": resolved_enquiries,
        "top_faqs": top_faqs
    }
