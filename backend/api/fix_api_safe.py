import os

path = r'E:\SecureAttend\apk_build\lib\core\api_client.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

correct_url = "Uri.parse('" + chr(36) + "baseUrl" + chr(36) + "endpoint'),"
content = content.replace("Uri.parse('\\''),", correct_url)
content = content.replace("Uri.parse('\\'),", correct_url)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
