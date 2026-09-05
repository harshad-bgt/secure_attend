import os

path = r'E:\SecureAttend\apk_build\lib\screens\student_profile.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("ApiClient.post('/students/profile', data:", "ApiClient.put('/students/profile', data:")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
