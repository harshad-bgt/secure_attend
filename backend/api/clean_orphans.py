import sqlite3

conn = sqlite3.connect('secureattend.db')
cursor = conn.cursor()
try:
    cursor.execute("DELETE FROM students WHERE roll_number LIKE '%COMP%'")
    cursor.execute("DELETE FROM faculty WHERE employee_id LIKE 'FAC10%'")
    cursor.execute("DELETE FROM parents")
    cursor.execute("DELETE FROM parent_student_links")
    cursor.execute("DELETE FROM student_enrollments")
    conn.commit()
    print('Cleaned up orphaned records successfully')
except Exception as e:
    print('Error:', e)
conn.close()
