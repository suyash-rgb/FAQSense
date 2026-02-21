import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_upload():
    print("Testing /faq/upload...")
    url = f"{BASE_URL}/faq/upload"
    files = {'file': ('test_faq.csv', open('test_faq.csv', 'rb'), 'text/csv')}
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 201

def test_ask():
    print("\nTesting /faq/ask...")
    url = f"{BASE_URL}/faq/ask"
    payload = {"question": "What is FAQSense?"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200 and "direct CSV lookup" in response.json().get("answer", "")

if __name__ == "__main__":
    try:
        if test_upload() and test_ask():
            print("\nVerification SUCCESSFUL!")
        else:
            print("\nVerification FAILED!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
