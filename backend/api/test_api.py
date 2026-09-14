from fastapi.testclient import TestClient
from main import app
from security import create_access_token

client = TestClient(app)
token = create_access_token(data={"sub": "364", "role": "FACULTY"})
response = client.get("/api/v1/faculty/364/subjects", headers={"Authorization": f"Bearer {token}"})
print("STATUS:", response.status_code)
print("JSON:", response.json())
