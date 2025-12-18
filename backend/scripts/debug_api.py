import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoints():
    # 1. Get accounts
    print("Testing GET /accounts")
    r = requests.get(f"{BASE_URL}/accounts/")
    if r.status_code != 200:
        print(f"FAILED: {r.status_code} - {r.text}")
        return
    
    accounts = r.json()
    if not accounts:
        print("No accounts found. Seed data first.")
        return
    
    acc_id = accounts[0]['id']
    print(f"Testing with Account ID: {acc_id}")
    
    # 2. Test Inputs for account
    print(f"Testing GET /inputs/accounts/{acc_id}")
    r = requests.get(f"{BASE_URL}/inputs/accounts/{acc_id}")
    if r.status_code != 200:
        print(f"FAILED /inputs: {r.status_code} - {r.text}")
    else:
        print(f"SUCCESS /inputs: {len(r.json())} items found")
        
    # 3. Test Contracts for account
    print(f"Testing GET /contracts/accounts/{acc_id}/contracts")
    r = requests.get(f"{BASE_URL}/contracts/accounts/{acc_id}/contracts")
    if r.status_code != 200:
        print(f"FAILED /contracts: {r.status_code} - {r.text}")
    else:
        print(f"SUCCESS /contracts: {len(r.json())} items found")

if __name__ == "__main__":
    test_endpoints()
