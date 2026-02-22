import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "user_semantic_test"

def setup_bot():
    # 1. Sync User
    requests.post(f"{BASE_URL}/webhooks/clerk", json={
        "type": "user.created",
        "data": {"id": USER_ID, "email_addresses": [{"email_address": "semantic@test.com"}]}
    })

    # 2. Create Bot
    bot_resp = requests.post(f"{BASE_URL}/chatbots/", 
                             json={"name": "SemanticBot"}, 
                             headers={"X-User-ID": USER_ID})
    bot_id = bot_resp.json()['id']
    
    # 3. Upload CSV
    # Questions: "What are your hours?", "Do you offer refunds?"
    csv_data = "Question,Answer\nWhat are your hours?,We are open 24/7.\nDo you offer refunds?,Yes within 30 days.\n"
    requests.post(f"{BASE_URL}/chatbots/{bot_id}/upload", 
                  files={'file': ('test.csv', csv_data, 'text/csv')}, 
                  headers={"X-User-ID": USER_ID})
    
    return bot_id

def test_semantic(bot_id):
    test_cases = [
        ("When is the shop open?", "We are open 24/7."), # Paraphrase of "What are your hours?"
        ("Can I get my money back?", "Yes within 30 days."), # Paraphrase of "Do you offer refunds?"
        ("At what time do you close?", "We are open 24/7."), # Paraphrase
        ("how do I return this?", "Yes within 30 days."), # Semantic match
        ("tell me a joke", "ERROR") # Neg
    ]

    print("\n--- Running Semantic Search (Paraphrasing) Tests ---")
    print("Note: The first request might take a few seconds as the model loads.")
    
    success_count = 0
    for query, expected in test_cases:
        url = f"{BASE_URL}/chatbots/{bot_id}/ask"
        start_time = time.time()
        resp = requests.post(url, json={"question": query})
        end_time = time.time()
        
        duration = end_time - start_time
        
        if resp.status_code == 200:
            actual = resp.json().get('answer')
            if actual == expected:
                print(f"✅ [{duration:.2f}s] Query: '{query}' -> Found: '{actual}'")
                success_count += 1
            else:
                print(f"❌ [{duration:.2f}s] Query: '{query}' -> Expected: '{expected}', Got: '{actual}'")
        else:
            if expected == "ERROR":
                print(f"✅ [{duration:.2f}s] Query: '{query}' -> Correctly returned 404")
                success_count += 1
            else:
                print(f"❌ [{duration:.2f}s] Query: '{query}' -> Failed with status {resp.status_code}")

    print(f"\nPassed {success_count}/{len(test_cases)} tests.")

if __name__ == "__main__":
    try:
        bid = setup_bot()
        test_semantic(bid)
    except Exception as e:
        print(f"Test Setup Failed: {e}")
