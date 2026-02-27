from sqlalchemy.orm import Session
from app.entities.platform import Enquiry
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate
from typing import List

def create_enquiry(db: Session, chatbot_id: int, enquiry_in: EnquiryCreate) -> Enquiry:
    """
    Service to handle direct database operations for visitor enquiries.
    """
    db_enquiry = Enquiry(
        chatbot_id=chatbot_id,
        query_text=enquiry_in.query_text,
        visitor_name=enquiry_in.visitor_name,
        visitor_email=enquiry_in.visitor_email,
        visitor_phone=enquiry_in.visitor_phone
    )
    db.add(db_enquiry)
    db.commit()
    db.refresh(db_enquiry)
    return db_enquiry

def get_chatbot_enquiries(db: Session, chatbot_id: int) -> List[Enquiry]:
    """
    Retrieve all enquiries for a specific chatbot.
    """
    return db.query(Enquiry).filter(Enquiry.chatbot_id == chatbot_id).all()

def update_enquiry(db: Session, enquiry_id: int, enquiry_update: EnquiryUpdate) -> Enquiry:
    """
    Update an enquiry's status or notes.
    """
    db_enquiry = db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
    if not db_enquiry:
        return None
    
    update_data = enquiry_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_enquiry, key, value)
    
    db.commit()
    db.refresh(db_enquiry)
    return db_enquiry

def get_enquiry(db: Session, enquiry_id: int) -> Enquiry:
    return db.query(Enquiry).filter(Enquiry.id == enquiry_id).first()
