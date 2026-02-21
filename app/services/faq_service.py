import pandas as pd
import os
from io import StringIO

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "faq.csv")

def save_faq_csv(file_content: str):
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Verify CSV format and columns with pandas
    df = pd.read_csv(StringIO(file_content))
    if "Question" not in df.columns or "Answer" not in df.columns:
        raise ValueError("CSV must contain 'Question' and 'Answer' columns")
    
    # Save to disk
    df.to_csv(CSV_FILE, index=False)
    return len(df)

def get_answer_from_csv(question: str):
    if not os.path.exists(CSV_FILE):
        return None
    
    df = pd.read_csv(CSV_FILE)
    
    # Case-insensitive search
    # We strip whitespace and normalize case for better matching
    result = df[df["Question"].str.lower().str.strip() == question.lower().strip()]
    
    if not result.empty:
        return result.iloc[0]["Answer"]
    return None
