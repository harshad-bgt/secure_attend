import sys
sys.path.append(".")
from fastapi.testclient import TestClient
from main import app
from database import get_db, SessionLocal
from models import User

client = TestClient(app)

db = SessionLocal()
user = db.query(User).filter(User.id == 364).first()

# We need to authenticate as the faculty
from security import create_access_token
from datetime import timedelta

access_token_expires = timedelta(minutes=30)
access_token = create_access_token(
    data={"sub": str(user.id)}, expires_delta=access_token_expires
)

headers = {"Authorization": f"Bearer {access_token}"}

try:
    print("----- REQUESTING /api/v1/faculty/364/subjects -----")
    response = client.get("/api/v1/faculty/364/subjects", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    import traceback
    print("EXCEPTION OCCURRED DURING REQUEST!")
    traceback.print_exc()

try:
    print("\n----- REQUESTING /api/v1/faculty/364 -----")
    response_profile = client.get("/api/v1/faculty/364", headers=headers)
    print(f"Status Code: {response_profile.status_code}")
    print(f"Response Body: {response_profile.json()}")
except Exception as e:
    import traceback
    print("EXCEPTION OCCURRED DURING PROFILE REQUEST!")
    traceback.print_exc()

