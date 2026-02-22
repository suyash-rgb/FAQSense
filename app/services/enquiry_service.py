from sqlalchemy.orm import Session
from app.models.platform import Enquiry
from app.schemas.enquiry import EnquiryCreate

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
