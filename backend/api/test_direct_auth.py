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

print("\n--- Testing GET /api/v1/auth/me ---")
res = client.get("/api/v1/auth/me", headers=headers)
print(f"Status Code: {res.status_code}")
print(f"Response Body: {res.text}")

