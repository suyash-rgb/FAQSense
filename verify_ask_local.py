import requests

def test_ask():
    # Try localhost
    url = "http://localhost:8000/chatbots/22/ask"
    payload = {
        "question": "refunds",
        "conversation_id": "test_session_123"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_ask()
