import requests
import sys

BASE_URL = "http://localhost:8000"

def register(username, password):
    url = f"{BASE_URL}/profiles/"
    try:
        resp = requests.post(url, json={"username": username, "password": password})
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 400 and "already registered" in resp.text:
            # Try login to get ID if already exists
            resp = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
            if resp.status_code == 200:
                token = resp.json()['access_token']
                # Get profile to get ID
                headers = {"Authorization": f"Bearer {token}"}
                profile_resp = requests.get(f"{BASE_URL}/profiles/me", headers=headers)
                return profile_resp.json()
    except Exception as e:
        print(f"Failed to register/login {username}: {e}")
    return None

def login(username, password):
    url = f"{BASE_URL}/token"
    resp = requests.post(url, data={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json()['access_token']
    return None

def create_plan(token, title):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{BASE_URL}/plans/", json={"title": title, "description": "test"}, headers=headers)
    return resp.json() if resp.status_code == 200 else None

def test_ownership():
    print("Test: Ownership Verification")
    
    # 1. Setup Users
    user1 = register("owner_user", "pass1")
    user2 = register("hacker_user", "pass2")
    
    if not user1 or not user2:
        print("Failed to setup users.")
        return

    token1 = login("owner_user", "pass1")
    token2 = login("hacker_user", "pass2")

    # 2. User 1 creates a plan
    plan = create_plan(token1, "Secret Plan")
    if not plan:
        print("Failed to create plan for User 1")
        return
    
    plan_id = plan['id']
    print(f"User 1 created Plan ID {plan_id}")

    # 3. User 2 tries to access User 1's plan (GET /plans/plan_id)
    # The current API for /plans/ usually lists all, but let's check specifics
    # The routers/plans.py might allow reading specific plan?
    # Let's try adding a macrocycle to User 1's plan as User 2
    
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    print(f"User 2 attempting to add Macrocycle to Plan {plan_id}...")
    resp = requests.post(
        f"{BASE_URL}/macrocycles/{plan_id}/", 
        json={"name": "Hacked Macro", "description": "should fail"},
        headers=headers2
    )
    
    if resp.status_code == 403:
        print("SUCCESS: User 2 was denied access (403 Forbidden).")
    else:
        print(f"FAILURE: User 2 got status {resp.status_code}. Response: {resp.text}")

if __name__ == "__main__":
    test_ownership()
