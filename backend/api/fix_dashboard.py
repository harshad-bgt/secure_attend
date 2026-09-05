import os

path = r'E:\SecureAttend\apk_build\lib\screens\student_dashboard.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken interpolation
content = content.replace("              'Good Morning, \\',", "              'Good Morning, ',")
content = content.replace("              'ID: \\',", "              'ID: ',")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
