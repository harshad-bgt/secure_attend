import os
path = r'E:\SecureAttend\backend\api\routes\students.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoint = '''
class StudentProfileUpdate(BaseModel):
    phone: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None

@router.put("/profile")
def update_student_profile(profile_data: StudentProfileUpdate, current_user: User = Depends(require_role(RoleName.STUDENT)), db: Session = Depends(get_db)):
    student = current_user.student_profile
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
        
    if profile_data.phone is not None:
        student.phone = profile_data.phone
    if profile_data.blood_group is not None:
        student.blood_group = profile_data.blood_group
    if profile_data.address is not None:
        student.address = profile_data.address
        
    db.commit()
    db.refresh(student)
    return {"status": "ok", "message": "Profile updated successfully"}
'''

if 'def update_student_profile' not in content:
    content += '\n' + new_endpoint
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
