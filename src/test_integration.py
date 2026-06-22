import requests
import json
import time

API_URL = "http://localhost:8000"

def test_health():
    print("\n--- Testing GET /health ---")
    res = requests.get(f"{API_URL}/health")
    print(f"Status Code: {res.status_code}")
    print(res.json())
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_valid_query():
    print("\n--- Testing POST /api/chat (Factual Query) ---")
    payload = {"query": "What is the exit load for the focused fund?"}
    res = requests.post(f"{API_URL}/api/chat", json=payload)
    print(f"Status Code: {res.status_code}")
    data = res.json()
    print(json.dumps(data, indent=2))
    assert res.status_code == 200
    assert data["status"] == "success"
    assert data["source_url"] is not None
    assert data["footer"] is not None
    assert "exit load" in data["response"].lower() or "applicable" in data["response"].lower()

def test_advisory_query():
    print("\n--- Testing POST /api/chat (Advisory/Refusal) ---")
    payload = {"query": "Should I invest in HDFC ELSS?"}
    res = requests.post(f"{API_URL}/api/chat", json=payload)
    print(f"Status Code: {res.status_code}")
    data = res.json()
    print(json.dumps(data, indent=2))
    assert res.status_code == 200
    assert data["status"] == "refused"
    assert "sebi-registered" in data["response"].lower() or "facts-only" in data["response"].lower()

def test_pii_query():
    print("\n--- Testing POST /api/chat (PII Refusal) ---")
    payload = {"query": "My email is test@example.com. Tell me the exit load of the focused fund."}
    res = requests.post(f"{API_URL}/api/chat", json=payload)
    print(f"Status Code: {res.status_code}")
    data = res.json()
    print(json.dumps(data, indent=2))
    assert res.status_code == 200
    assert data["status"] == "refused"
    assert "privacy warning" in data["response"].lower() or "pii" in data["response"].lower()

def test_rate_limiting():
    print("\n--- Testing Rate Limiting (rapid requests) ---")
    payload = {"query": "What is the minimum investment for large cap?"}
    
    # Send 40 rapid requests to trigger 429 (limit is 30/min)
    triggered = False
    for i in range(40):
        res = requests.post(f"{API_URL}/api/chat", json=payload)
        if res.status_code == 429:
            print(f"Rate limited successfully at request #{i+1} with status 429!")
            print(res.json())
            triggered = True
            break
        time.sleep(0.05)
    
    assert triggered, "Did not trigger rate limiting after 40 requests."

if __name__ == "__main__":
    print("============================================================")
    print("  RUNNING PHASE 4 BACKEND INTEGRATION TESTS")
    print("============================================================")
    
    test_health()
    test_valid_query()
    test_advisory_query()
    test_pii_query()
    
    # Wait a bit to clear previous hits so we don't trigger rate limiting prematurely
    time.sleep(1)
    test_rate_limiting()
    
    print("\n============================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY! ✅")
    print("============================================================")
