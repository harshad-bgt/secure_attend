import os

path = r'E:\SecureAttend\apk_build\lib\core\api_client.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
content = re.sub(
    r"Uri\.parse\('.*?'\),",
    "Uri.parse('\\'),",
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
