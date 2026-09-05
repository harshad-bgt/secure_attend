import os
path = r'E:\SecureAttend\backend\admin\src\pages\attendance\LiveSessionView.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
if 'Session ID: {sessionId}' not in content:
    content = content.replace('Live Session Active</h1>', 'Live Session Active</h1>\n            <p className=\"text-slate-500 mt-2\">Session ID: {sessionId}</p>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
