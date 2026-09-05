import sys
import os

# Add the api directory to the path so we can import from database and models
sys.path.append(os.path.join(os.path.dirname(__file__)))

from database import SessionLocal
from models import User
from security import get_password_hash

def update_admin():
    db = SessionLocal()
    try:
        # Check for old email
        user = db.query(User).filter(User.email == "admin@secureattend.ai").first()
        if user:
            user.email = "admin@depterp.ai"
            user.password_hash = get_password_hash("Admin123!")
            db.commit()
            print("Updated existing admin user from admin@secureattend.ai to admin@depterp.ai")
        else:
            # Check for new email in case it was already updated
            user = db.query(User).filter(User.email == "admin@depterp.ai").first()
            if user:
                user.password_hash = get_password_hash("Admin123!")
                db.commit()
                print("Updated password for admin@depterp.ai")
            else:
                print("Admin user not found!")
    except Exception as e:
        print(f"Error updating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin()
