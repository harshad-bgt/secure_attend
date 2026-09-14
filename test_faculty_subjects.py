import sys
import os

sys.path.append(os.path.abspath("backend/api"))

from database import SessionLocal
from models import FacultySubjectAssignment, Subject, Division

db = SessionLocal()

user_id = 364
assignments = db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).all()
print(f"Found {len(assignments)} assignments for {user_id}")

result = []
for a in assignments:
    subject = db.query(Subject).filter(Subject.id == a.subject_id).first()
    division = db.query(Division).filter(Division.id == a.division_id).first()
    print(f"  Assignment {a.id}: Subject: {subject is not None}, Division: {division is not None}")
    if subject and division:
        result.append({
            "assignment_id": a.id,
            "subject_id": subject.id,
            "subject_name": subject.name,
            "subject_code": subject.code,
            "division_id": division.id,
            "division_name": division.name
        })

print(f"Result count: {len(result)}")
