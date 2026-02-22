import os
import pandas as pd
import csv
from sqlalchemy.orm import Session
from app.models.platform import Chatbot, Enquiry
from app.schemas.chatbot import ChatbotCreate, ChatbotUpdate
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate
from io import StringIO
from typing import List, Optional
from app.services import engine_service, enquiry_service

DATA_DIR = "data"

def create_chatbot(db: Session, chatbot_in: ChatbotCreate, user_id: str) -> Chatbot:
    db_chatbot = Chatbot(
        name=chatbot_in.name,
        user_id=user_id,
        is_active=chatbot_in.is_active
    )
    db.add(db_chatbot)
    db.commit()
    db.refresh(db_chatbot)
    return db_chatbot

def get_user_chatbots(db: Session, user_id: str) -> List[Chatbot]:
    return db.query(Chatbot).filter(Chatbot.user_id == user_id).all()

def get_chatbot(db: Session, chatbot_id: int) -> Chatbot:
    return db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()

def validate_csv_content(file_content: str):
    f = StringIO(file_content)
    reader = csv.reader(f)
    try:
        header = next(reader)
    except StopIteration:
        raise ValueError("The uploaded CSV is empty")

    if len(header) != 2:
        raise ValueError(f"Invalid column count: Expected 2, found {len(header)}. Headers must be 'Question,Answer'")

    if header[0].strip() != "Question" or header[1].strip() != "Answer":
        raise ValueError(f"Invalid headers: Expected 'Question,Answer', found '{header[0]},{header[1]}'")

    line_num = 2
    for row in reader:
        if not any(row): continue
        if len(row) != 2:
            raise ValueError(f"Constraint Violation at row {line_num}: Expected 2 columns, found {len(row)}")
        if not row[0].strip() or not row[1].strip():
            raise ValueError(f"Empty value at row {line_num}: Both 'Question' and 'Answer' must be filled")
        line_num += 1
    return True

def save_chatbot_csv(db: Session, chatbot_id: int, file_content: str):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    file_path = os.path.join(DATA_DIR, f"chatbot_{chatbot_id}.csv")
    validate_csv_content(file_content)
    
    df = pd.read_csv(StringIO(file_content))
    df.to_csv(file_path, index=False)
    
    db_chatbot = get_chatbot(db, chatbot_id)
    if db_chatbot:
        db_chatbot.csv_file_path = file_path
        db.commit()
        db.refresh(db_chatbot)
    return len(df)

def get_answer_from_chatbot(chatbot: Chatbot, question: str) -> Optional[str]:
    """
    Orchestrates the answer retrieval by calling the specialized engine service.
    """
    if not chatbot.csv_file_path or not os.path.exists(chatbot.csv_file_path):
        return None
    
    # Delegate core search and matching logic to engine_service
    return engine_service.find_answer(chatbot.id, chatbot.csv_file_path, question)

def create_enquiry(db: Session, chatbot_id: int, enquiry_in: EnquiryCreate) -> Enquiry:
    """
    Orchestrates enquiry registration by calling the specialized enquiry service.
    """
    return enquiry_service.create_enquiry(db, chatbot_id, enquiry_in)

def get_enquiries(db: Session, chatbot_id: int) -> List[Enquiry]:
    """
    Orchestrates retrieving all enquiries for a specific chatbot.
    """
    return enquiry_service.get_chatbot_enquiries(db, chatbot_id)

def update_enquiry(db: Session, enquiry_id: int, enquiry_update: EnquiryUpdate) -> Enquiry:
    """
    Orchestrates updating an enquiry's status or notes.
    """
    return enquiry_service.update_enquiry(db, enquiry_id, enquiry_update)

def get_enquiry(db: Session, enquiry_id: int) -> Enquiry:
    return enquiry_service.get_enquiry(db, enquiry_id)

def delete_chatbot(db: Session, chatbot_id: int):
    db_chatbot = get_chatbot(db, chatbot_id)
    if db_chatbot:
        if db_chatbot.csv_file_path and os.path.exists(db_chatbot.csv_file_path):
            os.remove(db_chatbot.csv_file_path)
        db.delete(db_chatbot)
        db.commit()
    return True
