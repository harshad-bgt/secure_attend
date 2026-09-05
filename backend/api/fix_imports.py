import os
path = r'E:\SecureAttend\backend\api\models.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey', 'from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text')
content = content.replace('from sqlalchemy import String, Boolean, DateTime, ForeignKey', 'from sqlalchemy import String, Boolean, DateTime, ForeignKey, Float, Text')
content = content.replace('from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text', 'from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer')

if 'Float' not in content[:500]: # Approximate imports section
    content = 'from sqlalchemy import Float, Integer, Text\n' + content

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed imports!')
