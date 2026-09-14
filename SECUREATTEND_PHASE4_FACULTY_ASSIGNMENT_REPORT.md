# SecureAttend Phase 4 — Faculty Assignment Report

## 1. Final Status

COMPLETE

## 2. Existing Assignment State

- Assignments before Phase 4: 0
- Assignments created: 46
- Final assignment count: 46

## 3. Assignment Model

Reused the existing `FacultySubjectAssignment` architecture completely natively without creating any duplicate or parallel tables:
- `faculty_id` (ForeignKey to `faculty.user_id`)
- `subject_id` (ForeignKey to `subjects.id`)
- `semester_id` (ForeignKey to `semesters.id`)
- `division_id` (ForeignKey to `divisions.id`)

**Schema Enhancement**: Added a declarative unique constraint across (`faculty_id`, `subject_id`, `division_id`) to strictly enforce data isolation, utilizing Alembic `render_as_batch=True` successfully.

## 4. Faculty Distribution
A comprehensive distribution across the entire faculty pool was achieved via dynamic round-robin mapping logic tied tightly to semester mapping. *(Sample of assignments shown below; refer to the DB for all 46 rows).*
| Faculty ID | Faculty Name | Semester | Subject | Division |
|------------|--------------|----------|---------|----------|
| 2 | Alan Smith | 3 | Data Structures & Algorithms | A |
| 3 | Sarah Jones | 3 | Data Structures & Algorithms | B |
| 4 | Neha Mahajan | 3 | Data Structures & Algorithms Lab | A |
| 4 | Neha Mahajan | 7 | Machine Learning Operations (MLOPS) | A & B |
| 5 | Rohit Gawande | 3 | Data Structures & Algorithms Lab | B |
| 5 | Rohit Gawande | 7 | Deep Learning | A & B |
| 11 | Snehal Borkar | 3 | Fundamentals of Artificial Intelligence | A & B |
| 23 | Priyanka Khandekar | 7 | Project Phase II | A & B |
*(Etc., distributed across all 20+ faculty).*

## 5. Semester Distribution

**Semester 3 (Active: 1)**:
- Division A assignments: 7
- Division B assignments: 7

**Semester 5 (Active: 3)**:
- Division A assignments: 10
- Division B assignments: 10

**Semester 7 (Active: 5)**:
- Division A assignments: 6
- Division B assignments: 6

Total across all Active Divisions: 46.

## 6. Subject Coverage

**Semester 3**:
- Data Structures & Algorithms (Core)
- OOP (Core)
- Math for ML (Core)
- Fundamentals of AI (Core)
- Related Labs (DSA Lab, OOP Lab, Python Lab)

**Semester 5**:
- Theory of Computation (Core)
- DAA (Core)
- SEPM (Core)
- Foundation of ML (Core)
- Related Labs (DAA Lab, FML Lab)
- Base Electives (Program Elective 1, Open Elective 3, Minor Course 3)

**Semester 7**:
- MLOPS (Core)
- Deep Learning (Core)
- SEPM (Core)
- Project Phase II
- Professional Electives & Open Electives (Specific Options mapped; see Section 7)

## 7. Elective Allocation

In Semester 7, specific categorical options were handled cleanly rather than assigning every generic option to all classes:
- **Professional Elective**: Division A was allocated `Cyber Security`, while Division B was allocated `Generative AI`.
- **Open Elective**: Division A was allocated `Data Analytics with R`, while Division B was allocated `Cloud Services in AI`.

## 8. Unassigned Subjects

- Inactive semesters (4, 6, 8) and their corresponding subjects were securely ignored and left entirely unassigned, exactly adhering to Phase 4 bounds.
- Redundant / unallocated elective options in Semester 7 (e.g. `IoT and 5G Technology`, `Virtual & Augmented Reality`, `Introduction to Machine Learning`, `Introduction to Big Data`) were intentionally left unassigned as the divisions had their required allocations met.

## 9. Validation

- **Valid Faculty/Subject/Division references**: Verified manually via foreign-key JOINs on DB (e.g. Alan Smith assigned exactly to valid IDs).
- **Semester consistency**: Strictly respected (Assignments are only placed in Divisions whose `semester_id` matches the Subject's `semester_id`).
- **Department consistency**: Confirmed.
- **Uniqueness**: Alembic constraint added and functionally verified.

## 10. Idempotency

- **First run**: Mapped successfully; `Added: 46, Skipped: 0`.
- **Second run**: Successfully blocked duplicates and reused records securely; `Added: 0, Skipped: 46`.

## 11. Attendance / Face Safety

Verified via direct query:
- Attendance records created = 0
- Attendance sessions created = 0
- Face templates created = 0

## 12. Student Safety

Verified:
- Student records changed = 0
- StudentEnrollment records changed = 0

## 13. Build/Test

- **Backend**: Alembic migrated beautifully, API operates stably without routing mismatches.
- **Admin API Check**: Verified `GET /api/v1/faculty/<id>/subjects` pulls dynamic DB records appropriately for Faculty Profiles.
- **Frontend**: The `FacultyDetails.tsx` successfully reads the mapped assignments array into its table without breaking UI constraints. 
- `tsc -b` returned code 0 successfully.

## 14. Problems / Issues

None found. 

## 15. Final Status

COMPLETE
