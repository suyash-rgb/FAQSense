
import sys
import os
import pandas as pd

# Add the project root to sys.path
sys.path.append(r"d:\FAQSense\backend")

from app.services.engine_service import find_answer, get_keywords, CSV_DATA_CACHE
from app.core.config import settings

def setup_test_data():
    # Bot 1 Data
    df1 = pd.DataFrame({
        "Question": ["Do you offer refunds?", "How do I contact support?"],
        "Answer": ["Refunds are available within 30 days.", "Email support@faqsense.com"]
    })
    df1.to_csv("bot_1.csv", index=False)
    
    # Bot 2 Data (The "Wall" test)
    df2 = pd.DataFrame({
        "Question": ["What is your pricing?", "Where is your office?"],
        "Answer": ["Pricing starts at $10/mo.", "We are in San Francisco."]
    })
    df2.to_csv("bot_2.csv", index=False)
    return "bot_1.csv", "bot_2.csv"

def run_test(name, chatbot_id, csv_path, query, expected_match):
    print(f"\n--- [TEST] {name} ---")
    print(f"Query: '{query}'")
    answer, matched_q = find_answer(chatbot_id, csv_path, query)
    print(f"Result: {matched_q}")
    
    if matched_q == expected_match:
        print("✅ PASS")
    else:
        print(f"❌ FAIL (Expected: {expected_match})")

def main():
    csv1, csv2 = setup_test_data()
    
    # 1. Logic Gate 1: Absolute Precision (Exact Match)
    run_test("Exact Match (Case/Space)", 1, csv1, "  do you offer REFUNDS?  ", "Do you offer refunds?")
    
    # 2. Logic Gate 2: Typo Fixer (Fuzzy Match)
    # "refinds" should match "refunds" with high score and keyword overlap
    run_test("Fuzzy Match (Typo)", 1, csv1, "Do you offer refinds?", "Do you offer refunds?")
    
    # 3. Faithfulness A: Anti-Confusion (Multi-bot/Clean Wall)
    # Querying Bot 1 for Bot 2's specific data should return None
    run_test("Clean Wall (Bot Isolation)", 1, csv1, "What is your pricing?", None)
    
    # 4. Faithfulness B: Anti-Hallucination (Keyword Guardrail for Semantic)
    # A query that is semantically vague but might hit a low score (0.35 - 0.60) 
    # but has ZERO keywords should be rejected.
    # Note: With FastEmbed, it's hard to get < 0.6 for related-ish things, 
    # so we'll just verify the logic branch exists.
    run_test("Keyword Guard (Low Score/No Overlap)", 1, csv1, "Tell me about finances", None)
    
    # 5. Faithfulness C: Anti-Guessing (Score Gap/Ambiguity)
    # Let's add a bot with ambiguous questions
    df_ambig = pd.DataFrame({
        "Question": ["I want to buy a car", "I want to rent a car"],
        "Answer": ["Buying info...", "Renting info..."]
    })
    df_ambig.to_csv("bot_ambig.csv", index=False)
    # Query "I need a car" might hit both closely.
    # If the gap is < 0.05 and score < 0.6, it should return None.
    run_test("Ambiguity Gap", 3, "bot_ambig.csv", "I need a car", None)

    # Cleanup
    for f in ["bot_1.csv", "bot_2.csv", "bot_ambig.csv"]:
        if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    main()
