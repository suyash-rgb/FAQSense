import requests
import json

BASE_URL = "http://127.0.0.1:8000"
USER_ID = "user_fallback_test"

def setup_bot():
    # 1. Sync User
    requests.post(f"{BASE_URL}/webhooks/clerk", json={
        "type": "user.created",
        "data": {"id": USER_ID, "email_addresses": [{"email_address": "fallback@test.com"}]}
    })

    # 2. Create Bot
    bot_resp = requests.post(f"{BASE_URL}/chatbots/", 
                             json={"name": "FallbackBot"}, 
                             headers={"X-User-ID": USER_ID})
    bot_id = bot_resp.json()['id']
    
    # 3. Upload CSV
    csv_data = "Question,Answer\nWhat are your hours?,We are open 24/7."
    requests.post(f"{BASE_URL}/chatbots/{bot_id}/upload", 
                  files={'file': ('test.csv', csv_data, 'text/csv')}, 
                  headers={"X-User-ID": USER_ID})
    
    return bot_id

def test_fallback_and_enquiry(bot_id):
    print("\n--- Testing Fallback Message ---")
    query = "How do I build a rocket?" # Zero match
    resp = requests.post(f"{BASE_URL}/chatbots/{bot_id}/ask", json={"question": query})
    
    expected_fallback = "I did not understand that! Please try to rephrase your question or register your query with us."
    actual_answer = resp.json().get('answer')
    
    if actual_answer == expected_fallback:
        print(f"✅ Correct fallback received: '{actual_answer}'")
    else:
        print(f"❌ Incorrect fallback: Expected '{expected_fallback}', Got '{actual_answer}'")

    print("\n--- Testing Enquiry Registration ---")
    enquiry_data = {
        "query_text": query,
        "visitor_name": "Elon Musk",
        "visitor_email": "elon@spacex.com",
        "visitor_phone": "1234567890"
    }
    enq_resp = requests.post(f"{BASE_URL}/chatbots/{bot_id}/enquiries", json=enquiry_data)
    
    if enq_resp.status_code == 200:
        data = enq_resp.json()
        print(f"✅ Enquiry registered successfully: ID {data['id']}")
        print(f"   Name: {data['visitor_name']}, Email: {data['visitor_email']}, Phone: {data['visitor_phone']}")
    else:
        print(f"❌ Enquiry registration failed (Status {enq_resp.status_code}): {enq_resp.text}")

    print("\n--- Testing Partial Enquiry (Phone only) ---")
    partial_data = {
        "query_text": query,
        "visitor_name": "Jeff Bezos",
        "visitor_phone": "0987654321"
    }
    enq_resp2 = requests.post(f"{BASE_URL}/chatbots/{bot_id}/enquiries", json=partial_data)
    if enq_resp2.status_code == 200:
        print(f"✅ Partial enquiry (phone only) registered: ID {enq_resp2.json()['id']}")
    else:
        print(f"❌ Partial enquiry failed: {enq_resp2.text}")

if __name__ == "__main__":
    try:
        bid = setup_bot()
        test_fallback_and_enquiry(bid)
    except Exception as e:
        print(f"Test Failed: {e}")
