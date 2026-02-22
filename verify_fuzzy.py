import requests
import json

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "user_fuzzy_test"

def setup_bot():
    # 1. Sync User
    requests.post(f"{BASE_URL}/webhooks/clerk", json={
        "type": "user.created",
        "data": {"id": USER_ID, "email_addresses": [{"email_address": "fuzzy@test.com"}]}
    })

    # 2. Create Bot
    bot_resp = requests.post(f"{BASE_URL}/chatbots/", 
                             json={"name": "FuzzyBot"}, 
                             headers={"X-User-ID": USER_ID})
    bot_id = bot_resp.json()['id']
    
    # 3. Upload CSV
    csv_data = "Question,Answer\nWhat are your hours?,We are open 24/7.\nDo you offer refunds?,Yes within 30 days.\n"
    requests.post(f"{BASE_URL}/chatbots/{bot_id}/upload", 
                  files={'file': ('test.csv', csv_data, 'text/csv')}, 
                  headers={"X-User-ID": USER_ID})
    
    return bot_id

def test_fuzzy(bot_id):
    test_cases = [
        ("What are your hours?", "We are open 24/7."), # Exact
        ("what are your haors?", "We are open 24/7."), # Typo
        ("do u offer refun?", "Yes within 30 days."), # Typo/Slang
        ("hrs of operation?", "We are open 24/7."), # Semantic shift (partial match)
        ("completely unrelated string", "ERROR") # Neg
    ]

    print("\n--- Running Fuzzy Search Tests ---")
    success_count = 0
    for query, expected in test_cases:
        url = f"{BASE_URL}/chatbots/{bot_id}/ask"
        resp = requests.post(url, json={"question": query})
        
        if resp.status_code == 200:
            actual = resp.json().get('answer')
            if actual == expected:
                print(f"✅ Query: '{query}' -> Found: '{actual}'")
                success_count += 1
            else:
                print(f"❌ Query: '{query}' -> Expected: '{expected}', Got: '{actual}'")
        else:
            if expected == "ERROR":
                print(f"✅ Query: '{query}' -> Correctly returned 404")
                success_count += 1
            else:
                print(f"❌ Query: '{query}' -> Failed with status {resp.status_code}")

    print(f"\nPassed {success_count}/{len(test_cases)} tests.")

if __name__ == "__main__":
    try:
        bid = setup_bot()
        test_fuzzy(bid)
    except Exception as e:
        print(f"Test Setup Failed: {e}")
