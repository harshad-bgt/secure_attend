# SecureAttend Project Summary

## 1. PROJECT OVERVIEW
**Purpose:** SecureAttend is an AI-powered attendance system designed to manage student attendance securely using face recognition and dynamic QR codes.
**Target Users/Roles:** Admin, Faculty, Student (and a planned Parent role).
**Major Workflows:** 
- Admin/Faculty manage users and courses.
- Admin enrolls student faces via a web panel.
- Faculty generate dynamic QR codes for live attendance sessions.
- Students scan the QR code and verify their identity via face recognition on a mobile app to mark their attendance.
**Architecture:** Client-Server architecture with a web-based admin panel, a planned mobile app for students/faculty, and a centralized REST API backend.
**Technologies/Frameworks:**
- **Frontend:** React 19, Vite, TailwindCSS, React Router, React Query, React Webcam.
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic (for migrations).
- **Database:** SQLite (currently used as per `attendancedb.db` / `secureattend.db` files).
- **Authentication:** JWT (JSON Web Tokens) with Argon2 for password hashing.
- **Face Recognition:** `insightface` (using ONNX Runtime CPU) and OpenCV for face detection and embedding generation.

## 2. DIRECTORY / CODEBASE STRUCTURE
- `backend/`: The core project directory containing the server and admin panel.
  - `admin/`: Frontend React application (Vite).
    - `src/`: React source code (components, pages, routing).
    - `package.json`: Node dependencies.
  - `api/`: Backend FastAPI application.
    - `main.py`: Entry point for the FastAPI application, CORS setup, and global exception handlers.
    - `models.py`: SQLAlchemy database models representing all entities.
    - `schemas.py`: Pydantic models for request/response validation.
    - `routes/`: Contains API endpoint controllers (`auth.py`, `students.py`, `faculty.py`, `attendance.py`, `student_attendance.py`, `face_enrollment.py`, `erp.py`).
    - `services/`: Business logic, notably `face_service.py` for processing face images.
    - `database.py`: Database connection and session management.
    - `security.py`: Password hashing, JWT creation/verification, and QR token logic.
    - `dependencies.py`: Dependency injection functions like `get_current_user` and `require_role`.
    - `alembic/` & `alembic.ini`: Database migration scripts.
    - `requirements.txt`: Python dependencies.
  - `docs/`: Various documentation files (architecture, database schema, security, etc.).
  - `DEVELOPMENT_PROGRESS.md`: Tracks project completion phases and stages.
- `apk_build/`: (Empty/Not fully analyzed) Expected to hold the Flutter mobile application build.

## 3. IMPLEMENTED FEATURES
- **Authentication & Authorization (Fully Implemented):** Login, token refresh, and role-based access control.
- **User Management (Fully Implemented):** CRUD operations for students and faculty by Admins.
- **Face Enrollment (Fully Implemented):** Admins can upload images (via webcam or file) to generate and store face embeddings for students.
- **Live Attendance Sessions (Fully Implemented):** Faculty can start a session which generates a rotating dynamic QR code (refreshed every 60s).
- **Student Attendance Marking (Fully Implemented):** Students submit a captured photo (face verification) and a scanned QR token to mark themselves present.
- **ERP Base Features (Partially Implemented):** Timetable, Leaves, Achievements, and Notices routes exist but may lack complete frontend integration.

## 4. PHASE-WISE PROGRESS
According to the `DEVELOPMENT_PROGRESS.md` document, the project is structured in stages:
- **PROTOTYPE IMPLEMENTATION STAGE 1 — COMPLETED:** React Admin Panel scaffolding, full CRUD for Students/Faculty/Academic entities.
- **PROTOTYPE IMPLEMENTATION STAGE 2 — COMPLETED:** Admin-controlled Student Face Enrollment workflow utilizing `insightface` and SQLite BLOB storage.
- **PROTOTYPE IMPLEMENTATION STAGE 3 — COMPLETED:** Attendance session creation and backend-generated rotating Dynamic QR display on the Admin Panel.
- **PROTOTYPE IMPLEMENTATION STAGE 4 — COMPLETED:** Foundational Flutter Mobile UI, centralized API client, and Mobile dashboards.
- **PROTOTYPE IMPLEMENTATION STAGE 5 — PENDING/INCOMPLETE:** Finalizing missing backend endpoints and end-to-end integration (though the endpoints appear implemented in the codebase now, the stage was marked as next).

## 5. END-TO-END SYSTEM FLOW
**Admin Flow:** Login -> Admin Dashboard -> Manage Students -> Open Face Enrollment -> Capture Webcam Image -> Image sent to Backend -> `insightface` generates embedding -> Saved in DB -> Student profile updated.
**Faculty Flow:** Login -> Faculty Dashboard -> Select Subject/Division -> Start Session -> System displays Dynamic QR -> QR rotates every 60 seconds -> Session ended manually.
**Student Flow:** Login -> Student Dashboard -> Scan QR from Faculty Screen -> Capture Live Face -> Send QR Token + Face Image to Backend -> Backend verifies Face against Enrolled Template -> Backend validates QR expiration -> Attendance marked in DB.

## 6. AUTHENTICATION & USER MANAGEMENT
- **Login Flow:** `POST /api/v1/auth/login` validates email/password, returns access and refresh tokens.
- **Roles:** `ADMIN`, `FACULTY`, `STUDENT`, `PARENT`.
- **Password Storage:** Argon2 hashing (`security.py`).
- **Token Mechanism:** PyJWT. Refresh tokens are stored in the database (`RefreshToken` model) with a `family_id` to detect reuse and revoke compromised tokens.
- **Account Creation:** Students are created by Admins (`POST /api/v1/students/`). This automatically creates a `User` record and a linked `Student` profile.

## 7. STUDENT MANAGEMENT
- **Creation:** Admin provides email, password, roll number, first name, last name, and department ID.
- **Database Entities:** A `User` record (for auth) and a `Student` record (for profile details like roll number, blood group, address).
- **API Endpoints:** 
  - `POST /api/v1/students/` (Create)
  - `GET /api/v1/students/` (List)
  - `PUT /api/v1/students/profile` (Student updates own profile)
- **Unique Constraints:** `email` on User table, `roll_number` on Student table.

## 8. FACE ENROLLMENT / FACE RECOGNITION
- **Enrollment Workflow:** Admins capture/upload a student's photo via `POST /api/v1/students/{id}/face-enrollment`. Students can also self-enroll via `POST /api/v1/student/face-enrollment/enroll`.
- **Technology:** Python `insightface` (`buffalo_l` model) extracts embeddings.
- **Storage:** Embeddings are stored as raw bytes (BLOB/Text) in the `FaceTemplate` table, linked to `student_id`.
- **Verification:** During attendance, the captured face is compared against the enrolled embedding using cosine similarity (threshold 0.40). If successful, a short-lived `face_proof_token` is generated.

## 9. DATABASE ANALYSIS
**Models:**
- `User`: Base auth table (email, password_hash, role_id).
- `Role`, `Permission`, `RolePermission`: RBAC tables.
- `Student`, `Faculty`, `Parent`: Profile tables linked to `User.id` via Foreign Keys.
- `FaceTemplate`: Stores face embeddings linked to `Student.user_id`.
- `Department`, `Subject`, `AcademicYear`, `Semester`, `Division`: Academic taxonomy.
- `AttendanceSession`: Stores active sessions, current QR token, and expiry.
- `AttendanceRecord`: Links a `Student` to an `AttendanceSession`.

## 10. API INVENTORY
- `POST /auth/login`: Authenticate and get tokens.
- `POST /auth/refresh`: Rotate refresh tokens.
- `GET /auth/me`: Get current user profile.
- `POST /students/`: Create a student.
- `GET /students/`: List students.
- `POST /students/{id}/face-enrollment`: Admin enrolls face.
- `DELETE /students/{id}/face-enrollment`: Admin deletes face.
- `POST /student/face-enrollment/enroll`: Student self-enrolls face.
- `POST /attendance-sessions`: Create an attendance session.
- `GET /attendance-sessions/{id}/qr`: Get current rotating QR token.
- `POST /student/face-verification/verify`: Verify face and get `face_proof_token`.
- `POST /student/attendance/mark`: Submit QR token + face proof to mark present.

## 11. FRONTEND ANALYSIS
- **Framework:** React with Vite.
- **Styling:** TailwindCSS.
- **Pages:** Admin dashboard, Student listing, Faculty listing, Attendance sessions.
- **Integration:** Axios for API calls, React Query for state management and caching.
- **Uploads:** React Webcam is used for capturing photos.
- **Future Implication:** A "Bulk Student Import" feature would naturally fit in the Admin Dashboard's "Students" section as a new button/modal alongside the "Add Student" form.

## 12. BACKEND ANALYSIS
- **Architecture:** FastAPI standard directory structure (`routes`, `models`, `schemas`, `services`).
- **Data Flow:** Route -> Dependencies (`get_db`, `get_current_user`) -> Service (`face_service`) -> Repository/DB -> Response.
- **File Upload Handling:** FastAPI's `UploadFile` and `File(...)` are used for receiving image bytes in face enrollment/verification routes.
- **Exception Handling:** Global exception handlers in `main.py` log errors to `face_debug.log`.

## 13. EXISTING FILE UPLOAD / CSV / EXCEL CAPABILITIES
- **File Upload:** Functionality exists strictly for image uploads (`multipart/form-data`) using FastAPI's `UploadFile` in `face_enrollment.py` and `student_attendance.py`.
- **CSV/Excel Capabilities:** **NONE**. There is no existing CSV/Excel parser, nor any spreadsheet library (like `pandas` or `openpyxl`) in `requirements.txt`. There is no batch processing or bulk creation functionality currently implemented.

## 14. TESTING & VERIFICATION
- The codebase relies on manual testing or Postman/cURL, as there is no prominent test suite (like `pytest` tests) populated with comprehensive assertions, though a `tests/` folder exists.
- A `test_secureattend.db` indicates local SQLite testing.
- Several `seed_*.py` and `fix_*.py` scripts exist to seed mock data and patch database entries.

## 15. CONFIGURATION & ENVIRONMENT
- Environment variables are managed via `.env` (template `.env.example`).
- Configuration is loaded via `pydantic-settings` in `config.py`.
- Important settings include `JWT_SECRET_KEY`, `CORS_ORIGINS`, and database URLs. Secrets are not exposed in the codebase.

## 16. CURRENT LIMITATIONS / TECHNICAL DEBT
- **Face Model Loading:** `insightface` runs on CPU and initializes the model on startup/first request, which can cause significant latency on the first API call.
- **Logging:** Errors are hardcoded to write to `face_debug.log` instead of using a proper rotating logger.
- **Data Integrity:** Scripts like `fix_*.py` suggest there have been schema mismatches or data corruption during prototyping.
- **SQLite Concurrency:** The project uses SQLite which may struggle with concurrent writes (like 60 students marking attendance simultaneously).

## 17. IMPORTANT INTEGRATION POINTS FOR FUTURE FEATURES
- **Student Creation:** Any bulk import feature MUST adhere to the existing `POST /api/v1/students/` pattern: It must create a `User` entity (with hashed password) AND a `Student` entity.
- **Face Profile Flag:** When bulk creating students, `face_profile_active` must default to `False`.
- **Validation:** Imported students must have unique `email` and `roll_number` fields.
- **Rollback:** Bulk imports should be wrapped in a database transaction (`db.commit()` only if all rows are valid) to prevent partial creation.

## 18. FINAL PROJECT STATUS
**PROJECT:** SecureAttend
- **Architecture:** Client-Server
- **Frontend:** React, Vite, TailwindCSS (Admin Panel)
- **Backend:** Python, FastAPI
- **Database:** SQLite (via SQLAlchemy)
- **Authentication:** JWT, Argon2
- **Face Enrollment:** Implemented (InsightFace, SQLite BLOB)
- **Attendance:** Implemented (Dynamic QR + Face Verification)
- **Student Management:** Implemented (CRUD)
- **Faculty Management:** Implemented (CRUD)
- **Admin Management:** Implemented

**Completed phases:** Prototype Stages 1, 2, 3, 4 (as per `DEVELOPMENT_PROGRESS.md`).
**Remaining/incomplete phases:** Stage 5 (Mobile integration/Final testing).
**Major implemented features:** RBAC Auth, Student/Faculty CRUD, Web Face Enrollment, Live QR Attendance, Mobile Face Verification.
**Known limitations:** SQLite concurrency limits, lack of CSV/bulk import features, CPU-bound face recognition latency.
