# Database Schema Overview

The SecureAttend backend uses SQLite for its relational database, managed via SQLAlchemy (ORM) and Alembic (migrations). This document outlines the conceptual schema.

## Tables

### Users
Base table for all authenticated entities.
- `id` (PK)
- `email` (Unique, Indexed)
- `password_hash`
- `role` (Enum: ADMIN, FACULTY, STUDENT)
- `is_active`
- `created_at`
- `updated_at`

### Students
Inherits from / 1:1 with Users.
- `id` (PK, FK -> Users.id)
- `roll_number` (Unique, Indexed)
- `first_name`
- `last_name`
- `department_id` (FK)
- `face_profile_active` (Boolean)

### Faculty
Inherits from / 1:1 with Users.
- `id` (PK, FK -> Users.id)
- `employee_id` (Unique, Indexed)
- `first_name`
- `last_name`
- `department_id` (FK)

### Subjects
- `id` (PK)
- `code` (Unique)
- `name`
- `department_id` (FK)

### Schedules
Timetable entries mapping a subject to a faculty member for a specific time/class.
- `id` (PK)
- `subject_id` (FK)
- `faculty_id` (FK)
- `day_of_week`
- `start_time`
- `end_time`

### AttendanceSessions
Created when a faculty member starts an attendance window.
- `id` (PK)
- `schedule_id` (FK)
- `date`
- `start_time`
- `end_time`
- `status` (Enum: ACTIVE, ENDED)

### AttendanceRecords
The actual attendance marking for a student.
- `id` (PK)
- `session_id` (FK)
- `student_id` (FK)
- `timestamp`
- `status` (Enum: PRESENT, ABSENT)

### BiometricTemplates
Stores the face embeddings generated during enrollment.
- `id` (PK)
- `student_id` (FK, Unique)
- `embedding_data` (Blob/JSON)
- `version`
- `created_at`
