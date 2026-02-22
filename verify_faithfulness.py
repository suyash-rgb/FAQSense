import requests
import json

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "user_faithful_test"

def setup_bot():
    # 1. Sync User
    requests.post(f"{BASE_URL}/webhooks/clerk", json={
        "type": "user.created",
        "data": {"id": USER_ID, "email_addresses": [{"email_address": "faithful@test.com"}]}
    })

    # 2. Create Bot
    bot_resp = requests.post(f"{BASE_URL}/chatbots/", 
                             json={"name": "FaithfulBot"}, 
                             headers={"X-User-ID": USER_ID})
    bot_id = bot_resp.json()['id']
    
    # 3. Upload CSV with potentially confusing questions
    csv_data = (
        "Question,Answer\n"
        "What are your hours?,We are open 24/7.\n"
        "Do you offer refunds?,Yes within 30 days.\n"
        "How can I contact support?,Email us at support@test.com.\n"
        "How can I contact sales?,Email us at sales@test.com.\n" # Similar to support
    )
    requests.post(f"{BASE_URL}/chatbots/{bot_id}/upload", 
                  files={'file': ('test.csv', csv_data, 'text/csv')}, 
                  headers={"X-User-ID": USER_ID})
    
    return bot_id

def test_faithfulness(bot_id):
    test_cases = [
        # 1. Valid Paraphrase (Should Pass)
        ("When is the shop open?", "We are open 24/7."), 
        
        # 2. Ambiguity (Should Fail)
        # "How to contact them?" is close to both support and sales questions.
        # Score gap should be small.
        ("How to contact them?", "ERROR"), 
        
        # 3. No Keyword Overlap (Should Fail)
        # "When can I arrive?" might have a semantic score > 0.3 with "What are your hours?"
        # but if we determine there's no significant keyword match, it should fail.
        ("When can I move in?", "ERROR"), 
        
        # 4. Irrelevant (Should Fail)
        ("I like turtles", "ERROR")
    ]

    print("\n--- Running Faithfulness Check Tests ---")
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
                print(f"✅ Query: '{query}' -> Correctly rejected (Status {resp.status_code})")
                success_count += 1
            else:
                print(f"❌ Query: '{query}' -> Failed with status {resp.status_code}")

    print(f"\nPassed {success_count}/{len(test_cases)} tests.")

if __name__ == "__main__":
    try:
        bid = setup_bot()
        test_faithfulness(bid)
    except Exception as e:
        print(f"Test Setup Failed: {e}")
