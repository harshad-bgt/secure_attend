import sqlite3

conn = sqlite3.connect('secureattend.db')
cursor = conn.cursor()
try:
    cursor.execute("DELETE FROM users WHERE email LIKE 'student_%' OR email LIKE 'faculty_%' OR email LIKE 'parent_%'")
    conn.commit()
    print('Deleted all seeded users successfully')
except Exception as e:
    print('Error:', e)
conn.close()
