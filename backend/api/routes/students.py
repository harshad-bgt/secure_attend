from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from database import get_db
from models import Student, User, Role, RoleName, Department, AuditLog
from security import get_password_hash
from dependencies import require_role

router = APIRouter(prefix="/students", tags=["students"], dependencies=[Depends(require_role(RoleName.ADMIN))])

class StudentCreate(BaseModel):
    email: EmailStr
    password: str
    roll_number: str
    first_name: str
    last_name: str
    department_id: Optional[int] = None

class StudentResponse(BaseModel):
    user_id: int
    email: str
    roll_number: str
    first_name: str
    last_name: str
    is_active: bool
    department_id: Optional[int]

    model_config = {"from_attributes": True}

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(Student).filter(Student.roll_number == student.roll_number).first():
        raise HTTPException(status_code=400, detail="Roll number already exists")
        
    student_role = db.query(Role).filter(Role.name == RoleName.STUDENT).first()
    
    new_user = User(
        email=student.email,
        password_hash=get_password_hash(student.password),
        role_id=student_role.id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_student = Student(
        user_id=new_user.id,
        roll_number=student.roll_number,
        first_name=student.first_name,
        last_name=student.last_name,
        department_id=student.department_id
    )
    db.add(new_student)
    db.add(AuditLog(action="CREATE_STUDENT", target_resource="students", target_id=str(new_user.id)))
    db.commit()
    
    return {
        "user_id": new_user.id,
        "email": new_user.email,
        "roll_number": new_student.roll_number,
        "first_name": new_student.first_name,
        "last_name": new_student.last_name,
        "is_active": new_user.is_active,
        "department_id": new_student.department_id
    }

@router.get("/", response_model=List[StudentResponse])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).join(User).offset(skip).limit(limit).all()
    result = []
    for s in students:
        result.append({
            "user_id": s.user_id,
            "email": s.user.email,
            "roll_number": s.roll_number,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "is_active": s.user.is_active,
            "department_id": s.department_id
        })
    return result

@router.get("/{user_id}", response_model=StudentResponse)
def get_student(user_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    return {
        "user_id": student.user_id,
        "email": student.user.email,
        "roll_number": student.roll_number,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "is_active": student.user.is_active,
        "department_id": student.department_id
    }

@router.post("/{user_id}/toggle-status")
def toggle_student_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role.name != RoleName.STUDENT:
        raise HTTPException(status_code=404, detail="Student not found")
        
    user.is_active = not user.is_active
    db.add(AuditLog(action="TOGGLE_STUDENT_STATUS", target_resource="users", target_id=str(user.id), details=f"Active: {user.is_active}"))
    db.commit()
    return {"status": "success", "is_active": user.is_active}


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
