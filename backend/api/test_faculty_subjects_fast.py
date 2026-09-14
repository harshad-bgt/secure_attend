import sys
import json
from database import SessionLocal
from models import FacultySubjectAssignment, Subject, Division

db = SessionLocal()
user_id = 364
assignments = db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).all()
result = []
for a in assignments:
    subject = db.query(Subject).filter(Subject.id == a.subject_id).first()
    division = db.query(Division).filter(Division.id == a.division_id).first()
    if subject and division:
        result.append({
            "assignment_id": a.id,
            "subject_id": subject.id,
            "subject_name": subject.name,
            "subject_code": subject.code,
            "semester_id": a.semester_id,
            "division_id": division.id,
            "division_name": division.name
        })

print(json.dumps(result, indent=2))
