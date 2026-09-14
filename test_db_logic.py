import sqlite3

conn = sqlite3.connect("./backend/api/secureattend.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

user_id = 364

# Simulating: assignments = db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).all()
cursor.execute("SELECT * FROM faculty_subject_assignments WHERE faculty_id = ?", (user_id,))
assignments = cursor.fetchall()
print(f"Found {len(assignments)} assignments for {user_id}")

result = []
for a in assignments:
    # Simulating: subject = db.query(Subject).filter(Subject.id == a.subject_id).first()
    cursor.execute("SELECT * FROM subjects WHERE id = ?", (a["subject_id"],))
    subject = cursor.fetchone()
    
    # Simulating: division = db.query(Division).filter(Division.id == a.division_id).first()
    cursor.execute("SELECT * FROM divisions WHERE id = ?", (a["division_id"],))
    division = cursor.fetchone()
    
    print(f"  Assignment {a['id']}: Subject: {dict(subject) if subject else 'None'}, Division: {dict(division) if division else 'None'}")
    
    if subject and division:
        result.append({
            "assignment_id": a["id"],
            "subject_id": subject["id"],
            "subject_name": subject["name"],
            "subject_code": subject["code"],
            "division_id": division["id"],
            "division_name": division["name"]
        })

print(f"Final result: {result}")
