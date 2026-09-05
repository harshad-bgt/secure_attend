# ER Diagram — SecureAttend AI

## Entity-Relationship Diagram

```mermaid
erDiagram
    users ||--o{ refresh_tokens : has
    users ||--|| roles : has
    roles ||--o{ role_permissions : has
    permissions ||--o{ role_permissions : has

    users ||--o| students : "is"
    users ||--o| faculty : "is"

    departments ||--o{ students : contains
    departments ||--o{ faculty : contains
    departments ||--o{ subjects : offers

    academic_years ||--o{ semesters : contains
    semesters ||--o{ divisions : contains

    students ||--o{ student_enrollments : has
    subjects ||--o{ student_enrollments : enrolled_in
    divisions ||--o{ student_enrollments : in

    faculty ||--o{ faculty_subject_assignments : teaches
    subjects ||--o{ faculty_subject_assignments : assigned

    subjects ||--o{ timetable_entries : scheduled
    faculty ||--o{ timetable_entries : conducts
    classrooms ||--o{ timetable_entries : in
    divisions ||--o{ timetable_entries : for

    students ||--o{ face_profiles : has
    face_profiles ||--o{ face_enrollment_sessions : created_by
    face_enrollment_sessions ||--o{ face_enrollment_samples : contains

    students ||--o{ face_verification_events : has
    students ||--o{ liveness_verification_events : has

    timetable_entries ||--o{ attendance_sessions : generates
    faculty ||--o{ attendance_sessions : manages
    attendance_sessions ||--o{ attendance_records : contains
    students ||--o{ attendance_records : marked_for

    attendance_sessions ||--|| qr_session_secrets : has
    attendance_sessions ||--o{ qr_validation_logs : logs

    attendance_records ||--o{ attendance_corrections : corrected

    users ||--o{ notifications : receives
    users ||--o{ audit_logs : triggers

    users {
        int id PK
        string username UK
        string email UK
        string password_hash
        int role_id FK
        bool is_active
        datetime created_at
        datetime updated_at
    }

    students {
        int id PK
        int user_id FK UK
        int department_id FK
        string roll_number
        string enrollment_number
        int academic_year_id FK
        int semester_id FK
        int division_id FK
    }

    faculty {
        int id PK
        int user_id FK UK
        int department_id FK
        string employee_id UK
    }

    face_profiles {
        int id PK
        int student_id FK
        blob embedding
        int embedding_dim
        string model_name
        string model_version
        string status
        datetime activated_at
    }

    attendance_sessions {
        int id PK
        int timetable_entry_id FK
        int faculty_id FK
        string status
        datetime started_at
        datetime ended_at
    }

    attendance_records {
        int id PK
        int attendance_session_id FK
        int student_id FK
        string status
        datetime marked_at
        string device_hash
    }
```

## Key Relationships

| Relationship | Cardinality | Notes |
|-------------|-------------|-------|
| users → roles | N:1 | One role per user |
| users → students/faculty | 1:0..1 | Polymorphic profile by role |
| students → face_profiles | 1:N | Only one ACTIVE at a time |
| attendance_sessions → attendance_records | 1:N | UNIQUE(session, student) |
| timetable_entries → attendance_sessions | 1:N | Faculty starts session for a class |

## Soft Deletion

Entities with soft deletion (`deleted_at`):

- users (deactivation via `is_active` + optional `deleted_at`)
- students, faculty
- face_profiles (deactivation, not hard delete by default)

## Audit Trail Entities

- `audit_logs` — system-wide immutable events
- `face_verification_events` — per-verification attempt
- `liveness_verification_events` — per-liveness attempt
- `qr_validation_logs` — per-QR validation attempt
- `attendance_corrections` — admin manual corrections

See [DATABASE_SCHEMA.md](../database/DATABASE_SCHEMA.md) for full column definitions.
