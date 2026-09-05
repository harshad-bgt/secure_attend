import os
path = r'E:\SecureAttend\apk_build\lib\screens\student_profile.dart'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
d = chr(36)

# Fix Error line
content = re.sub(r"SnackBar\(content: Text\('Error:.*?\)\),", "SnackBar(content: Text('Error: " + d + "{e.toString()}')),", content)

# Fix Name line
content = re.sub(r"Text\(\s*\'\\ \',\s*textAlign: TextAlign.center,", "Text('" + d + "{profile[\'first_name\']} " + d + "{profile[\'last_name\']}', textAlign: TextAlign.center,", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
