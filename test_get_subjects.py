from fastapi.testclient import TestClient
from backend.api.main import app
from backend.api.database import get_db, SessionLocal
from backend.api.security import create_access_token
from backend.api.models import User

db = SessionLocal()
user = db.query(User).filter(User.id == 364).first()
token = create_access_token({"sub": str(user.id), "role": "FACULTY"})
db.close()

client = TestClient(app)
response = client.get("/faculty/364/subjects", headers={"Authorization": f"Bearer {token}"})
print("Status:", response.status_code)
print("Response:", response.json())
