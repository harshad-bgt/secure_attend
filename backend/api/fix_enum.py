import os
path = r'E:\SecureAttend\backend\api\models.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'PARENT = "PARENT"' not in content:
    content = content.replace('STUDENT = "STUDENT"', 'STUDENT = "STUDENT"\n    PARENT = "PARENT"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added PARENT to RoleName")
else:
    print("PARENT already exists")
