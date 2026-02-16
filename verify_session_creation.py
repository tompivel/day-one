import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv(".env")

BASE_URL = "http://localhost:8000"

def get_token(username, password):
    url = f"{BASE_URL}/token"
    resp = requests.post(url, data={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json()['access_token']
    print(f"Login failed: {resp.text}")
    return None

def test_create_session():
    print("Test: Session Creation Verification")
    
    username = "test_session_user" 
    password = "password123"
    
    # Register/Login
    requests.post(f"{BASE_URL}/profiles/", json={"username": username, "password": password})
    token = get_token(username, password)
    if not token: return

    headers = {"Authorization": f"Bearer {token}"}
    
    # Needs hierarchy: Plan -> Macro -> Micro
    # 1. Create Plan
    plan_resp = requests.post(f"{BASE_URL}/plans/", json={"title": "Session Test Plan"}, headers=headers)
    if plan_resp.status_code != 200:
        print(f"Failed to create plan: {plan_resp.text}")
        return
    plan_id = plan_resp.json()['id']
    
    # 2. Create Macro
    macro_resp = requests.post(f"{BASE_URL}/macrocycles/{plan_id}/", json={"name": "Macro 1"}, headers=headers)
    macro_id = macro_resp.json()['id']
    
    # 3. Create Micro
    micro_resp = requests.post(f"{BASE_URL}/microcycles/{macro_id}/", json={"name": "Micro 1"}, headers=headers)
    micro_id = micro_resp.json()['id']
    
    # 4. Create Session (Attempting with YYYY-MM-DD format as fixed in frontend)
    payload = {
        "description": "Test Session",
        "sport": "Running",
        "duration_minutes": 30,
        "date_start": "2026-02-17", # Plain date string
        "perceived_exertion": 5
    }
    
    print(f"Creating session for Microcycle {micro_id}...")
    resp = requests.post(f"{BASE_URL}/sessions/{micro_id}/", json=payload, headers=headers)
    
    if resp.status_code == 200:
        print(f"SUCCESS: Created Session ID {resp.json()['id']}")
        print(resp.json())
    else:
        print(f"FAILURE: Status {resp.status_code}. Response: {resp.text}")

if __name__ == "__main__":
    test_create_session()
