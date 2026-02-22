import os
import pandas as pd
import csv
from sqlalchemy.orm import Session
from app.models.platform import Chatbot, Enquiry
from app.schemas.chatbot import ChatbotCreate, ChatbotUpdate
from app.schemas.enquiry import EnquiryCreate
from io import StringIO
from typing import List, Optional
import re
import torch
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer, util
from app.core.config import settings

# Load a lightweight pre-trained model for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

# Simple in-memory cache for FAQ embeddings to avoid re-encoding on every request
EMBEDDING_CACHE = {} 

# Basic English stop words to ignore during keyword matching
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def get_keywords(text: str) -> set:
    """Extract significant lowercase words from text, ignoring stop words and punctuation."""
    import re
    words = re.findall(r'\b\w+\b', text.lower())
    return {w for w in words if w not in STOP_WORDS}

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
    
    # 1. Try Exact Match first (for performance and precision)
    result = df[df["Question"].str.lower().str.strip() == question.lower().strip()]
    if not result.empty:
        return result.iloc[0]["Answer"]
    
    # 2. If no exact match, try Fuzzy Match
    questions = df["Question"].tolist()
    # Using token_set_ratio for a more stable and less aggressive overlap check
    match = process.extractOne(
        question, 
        questions, 
        scorer=fuzz.token_set_ratio
    )
    
    if match:
        best_match, score, index = match
        if score >= settings.FUZZY_MATCH_THRESHOLD:
            # Add keyword guard even for fuzzy if not a perfect match
            query_keywords = get_keywords(question)
            match_keywords = get_keywords(best_match)
            overlap = query_keywords.intersection(match_keywords)
            
            if score > 95 or len(overlap) >= settings.MIN_KEYWORD_OVERLAP:
                return df.iloc[index]["Answer"]
    
    # 3. If no fuzzy match, try Semantic Match (Paraphrasing)
    
    cache_key = (chatbot.id, tuple(questions))
    
    if cache_key in EMBEDDING_CACHE:
        faq_embeddings = EMBEDDING_CACHE[cache_key]
    else:
        faq_embeddings = model.encode(questions, convert_to_tensor=True)
        EMBEDDING_CACHE[cache_key] = faq_embeddings
        
    query_embedding = model.encode(question, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    
    top_results = torch.topk(cos_scores, k=min(5, len(questions)))
    
    # Faithfulness Check 1: Rerank by Keyword Overlap
    # Even if semantic score is slightly lower, more keyword match is often better
    query_keywords = get_keywords(question)
    candidates = []
    
    for i in range(len(top_results.values)):
        idx = top_results.indices[i].item()
        score = top_results.values[i].item()
        matched_q = questions[idx]
        match_keywords = get_keywords(matched_q)
        overlap = query_keywords.intersection(match_keywords)
        
        candidates.append({
            'index': idx,
            'score': score,
            'overlap_count': len(overlap),
            'question': matched_q
        })
    
    # Sort by overlap count (primary) then semantic score (secondary)
    candidates.sort(key=lambda x: (x['overlap_count'], x['score']), reverse=True)
    
    best_candidate = candidates[0]
    best_score = best_candidate['score']
    best_index = best_candidate['index']
    
    # Faithfulness Check 2: Score Gap Analysis for Ambiguity
    if len(candidates) > 1:
        second_best = candidates[1]
        # Only check gap if they have the same overlap count (otherwise overlap count is the decider)
        if best_candidate['overlap_count'] == second_best['overlap_count']:
            gap = best_score - second_best['score']
            if gap < settings.AMBIGUITY_THRESHOLD:
                return None

    # Faithfulness Check 3: Threshold and Keyword Guard
    if best_score >= settings.SEMANTIC_MATCH_THRESHOLD:
        # If score is very high, we can be more lenient with keywords
        # If score is lower, we REQUIRE at least one keyword
        if best_score > settings.CONFIDENCE_THRESHOLD or best_candidate['overlap_count'] >= settings.MIN_KEYWORD_OVERLAP:
            return df.iloc[best_index]["Answer"]
            
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

def create_enquiry(db: Session, chatbot_id: int, enquiry_in: EnquiryCreate) -> Enquiry:
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
