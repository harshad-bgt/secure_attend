import os

path = r'E:\SecureAttend\apk_build\lib\screens\student_profile.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

correct_error = "SnackBar(content: Text('Error: " + chr(36) + "{e.toString()}')),"
content = content.replace("SnackBar(content: Text('Error: \\')),", correct_error)

correct_name = "'" + chr(36) + "{profile['first_name']} " + chr(36) + "{profile['last_name']}'"
content = content.replace("'\\'", correct_name)
# Wait, let's just use re.sub for any remaining "\'" if it matches that pattern.
# Actually I will just replace exactly what was broken.
import re
content = re.sub(r"SnackBar\(content: Text\('Error: \\'\)\),", correct_error, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
