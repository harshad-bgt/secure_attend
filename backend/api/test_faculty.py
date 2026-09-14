from database import SessionLocal
from models import FacultySubjectAssignment, Subject, Division, User

db = SessionLocal()

user_id = 364
assignments = db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).all()
print(f"Found {len(assignments)} assignments for {user_id}")

result = []
for a in assignments:
    subject = db.query(Subject).filter(Subject.id == a.subject_id).first()
    division = db.query(Division).filter(Division.id == a.division_id).first()
    print(f"  Assignment {a.id}: Subject: {subject is not None if subject else 'None'}, Division: {division is not None if division else 'None'}")
    if subject and division:
        result.append(a.id)

print(f"Result count: {len(result)}")
