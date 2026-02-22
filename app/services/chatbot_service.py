import os
import pandas as pd
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

def save_chatbot_csv(db: Session, chatbot_id: int, file_content: str):
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Path for this specific chatbot
    file_path = os.path.join(DATA_DIR, f"chatbot_{chatbot_id}.csv")
    
    # Verify CSV format with pandas
    df = pd.read_csv(StringIO(file_content))
    if "Question" not in df.columns or "Answer" not in df.columns:
        raise ValueError("CSV must contain 'Question' and 'Answer' columns")
    
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
