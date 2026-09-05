import os

path = r'E:\SecureAttend\apk_build\lib\core\api_client.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Uri.parse('\\'),", "Uri.parse('\\'),")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
