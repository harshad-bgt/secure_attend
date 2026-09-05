import os
path = r'E:\SecureAttend\backend\api\dependencies.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_deps = '''
from models import FacultyResponsibility

def require_admin():
    return require_role(RoleName.ADMIN)

def require_faculty():
    return require_role(RoleName.FACULTY)

def require_student():
    return require_role(RoleName.STUDENT)

def require_parent():
    return require_role(RoleName.PARENT)

def require_hod(current_user: User = Depends(require_faculty()), db: Session = Depends(get_db)):
    resp = db.query(FacultyResponsibility).filter_by(faculty_id=current_user.id).first()
    if not resp or not resp.is_hod:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires HOD privileges")
    return current_user

def require_amc(current_user: User = Depends(require_faculty()), db: Session = Depends(get_db)):
    resp = db.query(FacultyResponsibility).filter_by(faculty_id=current_user.id).first()
    if not resp or not resp.is_amc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires AMC privileges")
    return current_user

def require_gfm(current_user: User = Depends(require_faculty()), db: Session = Depends(get_db)):
    resp = db.query(FacultyResponsibility).filter_by(faculty_id=current_user.id).first()
    if not resp or not resp.is_gfm:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires GFM privileges")
    return current_user
'''

if 'def require_admin' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_deps)
    print("Added RBAC dependencies")
else:
    print("RBAC dependencies already exist")
