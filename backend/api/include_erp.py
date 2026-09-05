import os
path = r'E:\SecureAttend\backend\api\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'erp.router' not in content:
    content = content.replace('from routes import auth, students, faculty, academic, face_enrollment, attendance, student_attendance', 'from routes import auth, students, faculty, academic, face_enrollment, attendance, student_attendance, erp')
    
    if 'api_router.include_router(student_attendance.router)' in content:
        content = content.replace('api_router.include_router(student_attendance.router)', 'api_router.include_router(student_attendance.router)\napi_router.include_router(erp.router)')
    else:
        content += '\napi_router.include_router(erp.router)\n'
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
