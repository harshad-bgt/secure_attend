from fastapi.testclient import TestClient
from main import app
from database import SessionLocal
from models import CampusSettings, AttendanceRecord, AttendanceSession
from dependencies import get_db

client = TestClient(app)

def test_geofencing():
    print("Logging in admin...")
    response = client.post("/api/v1/auth/login", json={"email": "admin@secureattend.ai", "password": "Admin@123!"})
    assert response.status_code == 200
    admin_token = response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("Logging in faculty...")
    response = client.post("/api/v1/auth/login", json={"email": "faculty001@secureattend.demo", "password": "Admin@123!"})
    assert response.status_code == 200
    faculty_token = response.json()["access_token"]
    faculty_headers = {"Authorization": f"Bearer {faculty_token}"}

    print("Logging in student...")
    response = client.post("/api/v1/auth/login", json={"email": "student21b053@secureattend.demo", "password": "Admin@123!"})
    assert response.status_code == 200
    student_token = response.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    
    # Clean up any existing campus settings
    db = SessionLocal()
    db.query(CampusSettings).delete()
    db.commit()

    print("1. Starting Session...")
    response = client.post("/api/v1/admin/attendance-sessions", json={
        "faculty_id": 2, # Assuming faculty001 is user 2
        "subject_id": 1,
        "division_id": 1
    }, headers=faculty_headers)
    assert response.status_code == 200, response.text
    session_data = response.json()
    session_id = session_data["id"]
    qr_token = session_data["current_qr_token"]

    print("2. Mocking Face Proof...")
    # Generate a face proof token directly
    import jwt, datetime
    from datetime import timezone
    from config import get_settings
    s = get_settings()
    payload = {
        "sub": "356", # Assuming student is user 356
        "type": "face_proof",
        "exp": datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=5)
    }
    face_token = jwt.encode(payload, s.jwt_secret_key, algorithm="HS256")

    print("3. Attempt Attendance (Missing config)...")
    response = client.post("/api/v1/student/attendance/mark", json={
        "qr_token": qr_token,
        "face_proof_token": face_token,
        "latitude": 19.0,
        "longitude": 72.0
    }, headers=student_headers)
    assert response.status_code == 400, response.text
    assert "Campus geofence configuration is missing" in response.text
    print("-> Blocked due to missing config!")

    print("4. Set Admin Geofence Config...")
    response = client.post("/api/v1/admin/settings/geofence", json={
        "latitude": 19.0760,
        "longitude": 72.8777,
        "radius_meters": 500
    }, headers=admin_headers)
    assert response.status_code == 200, response.text
    print("-> Config set!")

    print("5. Attempt Attendance Outside Radius...")
    response = client.post("/api/v1/student/attendance/mark", json={
        "qr_token": qr_token,
        "face_proof_token": face_token,
        "latitude": 19.1000,
        "longitude": 72.8777
    }, headers=student_headers)
    assert response.status_code == 403, response.text
    assert "outside the campus geofence" in response.text
    print("-> Blocked outside radius!")

    print("6. Attempt Attendance Inside Radius...")
    response = client.post("/api/v1/student/attendance/mark", json={
        "qr_token": qr_token,
        "face_proof_token": face_token,
        "latitude": 19.0761,
        "longitude": 72.8778
    }, headers=student_headers)
    assert response.status_code == 200, response.text
    print("-> Accepted inside radius!")

    print("7. Attempt Duplicate Attendance...")
    response = client.post("/api/v1/student/attendance/mark", json={
        "qr_token": qr_token,
        "face_proof_token": face_token,
        "latitude": 19.0761,
        "longitude": 72.8778
    }, headers=student_headers)
    assert response.status_code == 409, response.text
    assert "Attendance already marked" in response.text
    print("-> Blocked duplicate!")

    print("Cleaning up...")
    response = client.post(f"/api/v1/admin/attendance-sessions/{session_id}/end", headers=faculty_headers)
    db.query(AttendanceRecord).filter(AttendanceRecord.attendance_session_id == session_id).delete()
    db.commit()
    print("All backend geofence logic successfully verified.")

if __name__ == "__main__":
    test_geofencing()
