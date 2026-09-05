import os

path = r'E:\SecureAttend\apk_build\lib\screens\student_profile.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
d = chr(36)
content = re.sub(r"Text\('Error: \\'\)", "Text('Error: " + d + "{e.toString()}')", content)
content = re.sub(r"SnackBar\(content: Text\('Error: \\'\)\),", "SnackBar(content: Text('Error: " + d + "{e.toString()}')),", content)
content = re.sub(r"\'\\ \\'", "'" + d + "{profile[\'first_name\']} " + d + "{profile[\'last_name\']}'", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
