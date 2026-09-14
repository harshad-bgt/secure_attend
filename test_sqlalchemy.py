import sys
import os
sys.path.append(os.path.abspath("backend/api"))
from database import SessionLocal
from models import FacultySubjectAssignment, Subject, Division
db = SessionLocal()
assignments = db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == 364).all()
print(f"Assignments found: {len(assignments)}")
for a in assignments:
    subject = db.query(Subject).filter(Subject.id == a.subject_id).first()
    division = db.query(Division).filter(Division.id == a.division_id).first()
    print(f"Subject: {subject is not None}, Division: {division is not None}")
