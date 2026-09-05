import os

path = r'E:\SecureAttend\backend\api\models.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update RoleName
if 'PARENT = "PARENT"' not in content:
    content = content.replace('STUDENT = "STUDENT"', 'STUDENT = "STUDENT"\n    PARENT = "PARENT"')

# 2. Add New Models
new_models = '''
# --- DeptERP Expanded Models ---

class FacultyResponsibility(Base):
    __tablename__ = "faculty_responsibilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.user_id", ondelete="CASCADE"), unique=True)
    is_hod: Mapped[bool] = mapped_column(Boolean, default=False)
    is_amc: Mapped[bool] = mapped_column(Boolean, default=False)
    is_gfm: Mapped[bool] = mapped_column(Boolean, default=False)
    
    faculty: Mapped["Faculty"] = relationship(backref="responsibilities")

class Parent(Base):
    __tablename__ = "parents"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    address: Mapped[Optional[str]] = mapped_column(Text)
    
    user: Mapped["User"] = relationship(backref="parent_profile")
    student_links: Mapped[List["ParentStudentLink"]] = relationship(back_populates="parent")

class ParentStudentLink(Base):
    __tablename__ = "parent_student_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.user_id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id", ondelete="CASCADE"))
    relation: Mapped[str] = mapped_column(String(50)) # e.g. "Father", "Mother", "Guardian"
    
    parent: Mapped["Parent"] = relationship(back_populates="student_links")
    student: Mapped["Student"] = relationship(backref="parent_links")

class GFMGroup(Base):
    __tablename__ = "gfm_groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.user_id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))
    
    gfm: Mapped["Faculty"] = relationship(backref="gfm_groups")
    students: Mapped[List["GFMStudentMapping"]] = relationship(back_populates="group")

class GFMStudentMapping(Base):
    __tablename__ = "gfm_student_mappings"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("gfm_groups.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id", ondelete="CASCADE"), unique=True)
    
    group: Mapped["GFMGroup"] = relationship(back_populates="students")
    student: Mapped["Student"] = relationship(backref="gfm_mapping")

class InternalMark(Base):
    __tablename__ = "internal_marks"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id", ondelete="CASCADE"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.user_id", ondelete="SET NULL"), nullable=True)
    marks_obtained: Mapped[float] = mapped_column(Float)
    total_marks: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50), default="PENDING_APPROVAL") # PENDING_APPROVAL, APPROVED, REJECTED
    
    student: Mapped["Student"] = relationship(backref="internal_marks")
    subject: Mapped["Subject"] = relationship()
    faculty: Mapped["Faculty"] = relationship()

class OfficialResult(Base):
    __tablename__ = "official_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id", ondelete="CASCADE"))
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id", ondelete="CASCADE"))
    sgpa: Mapped[Optional[float]] = mapped_column(Float)
    cgpa: Mapped[Optional[float]] = mapped_column(Float)
    percentage: Mapped[Optional[float]] = mapped_column(Float)
    has_backlog: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(50), default="PUBLISHED")
    
    student: Mapped["Student"] = relationship(backref="official_results")

class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.user_id", ondelete="CASCADE"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id", ondelete="CASCADE"))
    day_of_week: Mapped[int] = mapped_column(Integer) # 0 = Monday, 6 = Sunday
    start_time: Mapped[str] = mapped_column(String(5)) # HH:MM
    end_time: Mapped[str] = mapped_column(String(5)) # HH:MM
    room: Mapped[Optional[str]] = mapped_column(String(50))
    
    subject: Mapped["Subject"] = relationship()
    faculty: Mapped["Faculty"] = relationship()
    division: Mapped["Division"] = relationship()

class SyllabusDocument(Base):
    __tablename__ = "syllabus_documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"))
    file_url: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    subject: Mapped["Subject"] = relationship(backref="syllabus")

class DepartmentDocument(Base):
    __tablename__ = "department_documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200))
    file_url: Mapped[str] = mapped_column(String(500))
    document_type: Mapped[str] = mapped_column(String(50)) # e.g. "CIRCULAR", "POLICY"
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculty.user_id", ondelete="CASCADE"))
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, APPROVED, REJECTED
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    faculty: Mapped["Faculty"] = relationship(backref="leave_requests")

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.user_id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text)
    date_achieved: Mapped[Optional[datetime]] = mapped_column(DateTime)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=True) # Locks on submit
    
    student: Mapped["Student"] = relationship(backref="achievements")

class Notice(Base):
    __tablename__ = "notices"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    target_audience: Mapped[str] = mapped_column(String(100)) # e.g. "ALL", "STUDENTS", "FACULTY", "SE", "PARENTS"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    sender: Mapped["User"] = relationship()
'''

if 'class FacultyResponsibility(Base):' not in content:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_models)
    print("Appended new models successfully!")
else:
    print("New models already exist.")
