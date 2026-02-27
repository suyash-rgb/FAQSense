
import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.append(r"d:\FAQSense\backend")

from app.services.engine_service import find_answer

def test_variant_ambiguity():
    csv_path = "test_variants.csv"
    # Same answer, two different question phrasings
    df = pd.DataFrame({
        "Question": ["What are your hours?", "When are you open?"],
        "Answer": ["We are open 24/7.", "We are open 24/7."]
    })
    df.to_csv(csv_path, index=False)
    
    query = "Opening times?"
    print(f"Testing Query: '{query}'")
    
    answer, matched_q = find_answer(888, csv_path, query)
    
    if answer:
        print(f"✅ SUCCESS: Returned answer: '{answer}'")
    else:
        print(f"❌ FAIL: Ambiguity guard triggered fallback for variants of the same answer.")

    if os.path.exists(csv_path): os.remove(csv_path)

if __name__ == "__main__":
    test_variant_ambiguity()
