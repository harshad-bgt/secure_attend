import requests
import json

login_data = {
    "email": "faculty001@secureattend.demo",
    "password": "password"
}

print("Attempting to login...")
res = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json=login_data)
if res.status_code != 200:
    print("Login failed:", res.status_code, res.text)
    exit(1)

token = res.json()["access_token"]
print("Login successful.")

headers = {
    "Authorization": f"Bearer {token}"
}

print("\n--- TASK 2: Testing GET /api/v1/faculty/364/subjects ---")
try:
    api_res = requests.get("http://127.0.0.1:8000/api/v1/faculty/364/subjects", headers=headers)
    print(f"Status Code: {api_res.status_code}")
    print(f"Response Body: {api_res.text}")
except Exception as e:
    print("Error:", e)

print("\n--- TASK 9: Testing GET /api/v1/faculty/364 ---")
try:
    api_res2 = requests.get("http://127.0.0.1:8000/api/v1/faculty/364", headers=headers)
    print(f"Status Code: {api_res2.status_code}")
    print(f"Response Body: {api_res2.text}")
except Exception as e:
    print("Error:", e)
