import os
import pandas as pd
import torch
import re
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer, util
from app.core.config import settings

# Load a lightweight pre-trained model for semantic search
model = SentenceTransformer(settings.MODEL_PATH)

# Simple in-memory cache for FAQ embeddings to avoid re-encoding on every request
EMBEDDING_CACHE = {} 

# Reactive Cache for CSV Data
# Structure: { chatbot_id: {"df": pd.DataFrame, "mtime": float} }
CSV_DATA_CACHE = {}

def get_cached_df(chatbot_id: int, csv_path: str) -> pd.DataFrame:
    """Retrieve DataFrame from cache or load from disk if modified."""
    current_mtime = os.path.getmtime(csv_path)
    cached_entry = CSV_DATA_CACHE.get(chatbot_id)

    if not cached_entry or current_mtime > cached_entry["mtime"]:
        # Reload DF from disk
        df = pd.read_csv(csv_path)
        CSV_DATA_CACHE[chatbot_id] = {
            "df": df,
            "mtime": current_mtime
        }
    return CSV_DATA_CACHE[chatbot_id]["df"]

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
    words = re.findall(r'\b\w+\b', text.lower())
    return {w for w in words if w not in STOP_WORDS}

from typing import Tuple, Optional

def find_answer(chatbot_id: int, csv_path: str, question: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Core engine logic for finding the best answer using a hybrid approach.
    Returns: (AnswerText, OriginalFAQQuestion)
    """
    if not os.path.exists(csv_path):
        return None, None
    
    df = get_cached_df(chatbot_id, csv_path)
    questions = df["Question"].tolist()
    
    # 1. Exact Match
    result = df[df["Question"].str.lower().str.strip() == question.lower().strip()]
    if not result.empty:
        matched_q = result.iloc[0]["Question"]
        return result.iloc[0]["Answer"], matched_q
    
    # 2. Fuzzy Match
    match = process.extractOne(
        question, 
        questions, 
        scorer=fuzz.token_set_ratio
    )
    
    if match:
        best_match, score, index = match
        if score >= settings.FUZZY_MATCH_THRESHOLD:
            query_keywords = get_keywords(question)
            match_keywords = get_keywords(best_match)
            overlap = query_keywords.intersection(match_keywords)
            
            if score > 95 or len(overlap) >= settings.MIN_KEYWORD_OVERLAP:
                return df.iloc[index]["Answer"], best_match
    
    # 3. Semantic Match
    cache_key = (chatbot_id, tuple(questions))
    
    if cache_key in EMBEDDING_CACHE:
        faq_embeddings = EMBEDDING_CACHE[cache_key]
    else:
        faq_embeddings = model.encode(questions, convert_to_tensor=True)
        EMBEDDING_CACHE[cache_key] = faq_embeddings
        
    query_embedding = model.encode(question, convert_to_tensor=True)
    cos_scores = util.cos_sim(query_embedding, faq_embeddings)[0]
    
    top_results = torch.topk(cos_scores, k=min(5, len(questions)))
    
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
    
    # Rerank by overlap count (primary) then semantic score (secondary)
    candidates.sort(key=lambda x: (x['overlap_count'], x['score']), reverse=True)
    
    best_candidate = candidates[0]
    best_score = best_candidate['score']
    best_index = best_candidate['index']
    best_q = best_candidate['question']
    
    # Score Gap Analysis (Ambiguity)
    if len(candidates) > 1:
        second_best = candidates[1]
        if best_candidate['overlap_count'] == second_best['overlap_count']:
            gap = best_score - second_best['score']
            if gap < settings.AMBIGUITY_THRESHOLD:
                return None, None

    # Threshold and Keyword Guard
    if best_score >= settings.SEMANTIC_MATCH_THRESHOLD:
        if best_score > settings.CONFIDENCE_THRESHOLD or best_candidate['overlap_count'] >= settings.MIN_KEYWORD_OVERLAP:
            return df.iloc[best_index]["Answer"], best_q
            
    return None, None
