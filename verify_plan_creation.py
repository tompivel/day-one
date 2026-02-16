import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

BASE_URL = "http://localhost:8000"

def get_token(username, password):
    url = f"{BASE_URL}/token"
    resp = requests.post(url, data={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json()['access_token']
    print(f"Login failed: {resp.text}")
    return None

def test_create_plan():
    print("Test: Plan Creation Verification")
    
    # 1. Login (assuming user exists from previous steps, or register new)
    username = "test_plan_user" 
    password = "password123"
    
    # Register/Login flow
    reg_url = f"{BASE_URL}/profiles/"
    requests.post(reg_url, json={"username": username, "password": password})
    
    token = get_token(username, password)
    if not token:
        return

    # 2. Create Plan using correct endpoint POST /plans/
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"title": "Verified Plan", "description": "Created via verification script"}
    
    print(f"Attempting to create plan at {BASE_URL}/plans/ ...")
    resp = requests.post(f"{BASE_URL}/plans/", json=payload, headers=headers)
    
    if resp.status_code == 200:
        plan = resp.json()
        print(f"SUCCESS: Created Plan ID {plan['id']}")
        print(plan)
    else:
        print(f"FAILURE: Status {resp.status_code}. Response: {resp.text}")

if __name__ == "__main__":
    test_create_plan()
