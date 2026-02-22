import os
import pandas as pd
import csv
from sqlalchemy.orm import Session
from app.models.platform import Chatbot
from app.schemas.chatbot import ChatbotCreate, ChatbotUpdate
from io import StringIO
from typing import List

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
    """
    Manually validate that the CSV has exactly 2 columns in every row
    and the correct headers.
    """
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

    line_num = 2 # Starting from row 2
    for row in reader:
        if not any(row): # Skip empty lines
            continue
        if len(row) != 2:
            raise ValueError(f"Constraint Violation at row {line_num}: Expected 2 columns, found {len(row)}")
        
        if not row[0].strip() or not row[1].strip():
            raise ValueError(f"Empty value at row {line_num}: Both 'Question' and 'Answer' must be filled")
        
        line_num += 1
    
    return True

def save_chatbot_csv(db: Session, chatbot_id: int, file_content: str):
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Path for this specific chatbot
    file_path = os.path.join(DATA_DIR, f"chatbot_{chatbot_id}.csv")
    
    # Perform strict manual validation
    validate_csv_content(file_content)
    
    # If validation passes, we can safely load into Pandas
    df = pd.read_csv(StringIO(file_content))
    
    # Save to disk
    df.to_csv(file_path, index=False)
    
    # Update DB with file path
    db_chatbot = get_chatbot(db, chatbot_id)
    if db_chatbot:
        db_chatbot.csv_file_path = file_path
        db.commit()
        db.refresh(db_chatbot)
    
    return len(df)

def get_answer_from_chatbot(chatbot: Chatbot, question: str):
    if not chatbot.csv_file_path or not os.path.exists(chatbot.csv_file_path):
        return None
    
    df = pd.read_csv(chatbot.csv_file_path)
    
    # Case-insensitive search
    result = df[df["Question"].str.lower().str.strip() == question.lower().strip()]
    
    if not result.empty:
        return result.iloc[0]["Answer"]
    return None

def delete_chatbot(db: Session, chatbot_id: int):
    db_chatbot = get_chatbot(db, chatbot_id)
    if db_chatbot:
        # 1. Remove the CSV file from disk
        if db_chatbot.csv_file_path and os.path.exists(db_chatbot.csv_file_path):
            os.remove(db_chatbot.csv_file_path)
        
        # 2. Delete the database record
        db.delete(db_chatbot)
        db.commit()
    return True
