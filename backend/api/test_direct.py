import sys
sys.path.append('.')
from security import create_access_token
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Generate token for user 364
access_token = create_access_token(data={"sub": "364", "role": "FACULTY"})

headers = {
    "Authorization": f"Bearer {access_token}"
}

print("\n--- TASK 2: Testing GET /api/v1/faculty/364/subjects ---")
res = client.get("/api/v1/faculty/364/subjects", headers=headers)
print(f"Status Code: {res.status_code}")
print(f"Response Body: {res.text}")

print("\n--- TASK 9: Testing GET /api/v1/faculty/364 ---")
res2 = client.get("/api/v1/faculty/364", headers=headers)
print(f"Status Code: {res2.status_code}")
print(f"Response Body: {res2.text}")

