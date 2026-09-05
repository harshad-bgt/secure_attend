from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database import get_db
from models import Department, Subject, AcademicYear, Semester, Division, RoleName
from dependencies import require_role

router = APIRouter(prefix="/academic", tags=["academic"], dependencies=[Depends(require_role(RoleName.ADMIN, RoleName.FACULTY))])

# Models
class DepartmentCreate(BaseModel):
    code: str
    name: str

class DepartmentResponse(DepartmentCreate):
    id: int
    model_config = {"from_attributes": True}

class SubjectCreate(BaseModel):
    code: str
    name: str
    department_id: int

class SubjectResponse(SubjectCreate):
    id: int
    model_config = {"from_attributes": True}

class DivisionResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}

# Endpoints
@router.post("/departments", response_model=DepartmentResponse)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
    if db.query(Department).filter(Department.code == dept.code).first():
        raise HTTPException(status_code=400, detail="Department code already exists")
    db_dept = Department(**dept.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get("/departments", response_model=List[DepartmentResponse])
def list_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(subj: SubjectCreate, db: Session = Depends(get_db)):
    if db.query(Subject).filter(Subject.code == subj.code).first():
        raise HTTPException(status_code=400, detail="Subject code already exists")
    db_subj = Subject(**subj.model_dump())
    db.add(db_subj)
    db.commit()
    db.refresh(db_subj)
    return db_subj

@router.get("/subjects", response_model=List[SubjectResponse])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

@router.get("/divisions", response_model=List[DivisionResponse])
def list_divisions(db: Session = Depends(get_db)):
    return db.query(Division).all()
