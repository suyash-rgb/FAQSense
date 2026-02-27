
import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.append(r"d:\FAQSense\backend")

from app.services.engine_service import find_answer
from app.core.config import settings

def test_variant_aware_ambiguity():
    csv_path = "test_variant_aware.csv"
    
    print(f"--- [TEST] Variant-Aware Ambiguity ---")
    print(f"Ambiguity Threshold: {settings.AMBIGUITY_THRESHOLD}")

    # Case 1: Variants of the SAME answer (Should PASS)
    df_same = pd.DataFrame({
        "Question": ["What are your hours?", "When are you open?"],
        "Answer": ["We are open 24/7.", "We are open 24/7."]
    })
    df_same.to_csv(csv_path, index=False)
    
    query = "Opening times?"
    print(f"\nScenario 1: Variants phrasings for SAME answer")
    ans, q = find_answer(997, csv_path, query)
    if ans:
        print(f"✅ SUCCESS: Correctly ignored ambiguity for variants. Answer: '{ans}'")
    else:
        print(f"❌ FAIL: Ambiguity guard blocked identical answers.")

    # Case 2: Truly different answers with close scores (Should FAIL/FALLBACK)
    df_diff = pd.DataFrame({
        "Question": ["I want to buy a car", "I want to rent a car"],
        "Answer": ["Buying info...", "Renting info..."]
    })
    df_diff.to_csv(csv_path, index=False)
    
    query = "I need a car"
    print(f"\nScenario 2: Similar phrasing for DIFFERENT answers")
    ans, q = find_answer(998, csv_path, query)
    if ans is None:
        print(f"✅ SUCCESS: Correctly blocked ambiguous query for different intents.")
    else:
        print(f"❌ FAIL: Ambiguity guard allowed a risky guess for different answers. Result: '{ans}'")

    if os.path.exists(csv_path): os.remove(csv_path)

if __name__ == "__main__":
    test_variant_aware_ambiguity()
