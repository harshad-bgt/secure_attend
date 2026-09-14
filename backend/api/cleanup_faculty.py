import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))
from database import SessionLocal
from models import Faculty, User, FacultySubjectAssignment, RefreshToken

def cleanup_faculty():
    db = SessionLocal()
    try:
        faculty_to_delete = db.query(Faculty).filter(Faculty.employee_id.in_(["F1001", "F1002"])).all()
        count = 0
        for f in faculty_to_delete:
            user_id = f.user_id
            db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).delete()
            db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
            db.delete(f)
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
            count += 1
        db.commit()
        print(f"Cleaned up {count} old faculty records.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_faculty()
