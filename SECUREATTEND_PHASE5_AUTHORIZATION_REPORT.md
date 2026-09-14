# SECUREATTEND_PHASE5_AUTHORIZATION_REPORT.md

## 1. Final Status
COMPLETE

## 2. Authentication Architecture
The system uses JWT (JSON Web Tokens) where the authenticated identity is decoded into a `TokenPayload(sub, role, type)`. The `sub` maps to `User.id` and the `role` maps to `RoleName` (`ADMIN`, `FACULTY`, `STUDENT`). 

## 3. Authorization Architecture
Authorization is strictly enforced at the **query level**.
- **Admin**: The `require_admin` dependency unconditionally permits operations without data scope constraints.
- **Faculty**: Faculty users pass through `require_admin_or_faculty` but are subject to data masking through dynamically injected `.filter()` clauses on SQLAlchemy queries using scopes gathered from `get_faculty_scopes(faculty_id)`.

## 4. Faculty Scope
`FacultySubjectAssignment.faculty_id` correctly references `faculty.user_id` (which shares the identical ID with `User`). The `get_faculty_scopes()` helper determines a faculty's allowed `divisions`, `subjects`, and `semesters`. Multiple assignments correctly produce a mathematical UNION of these IDs automatically.

## 5. Student API
Faculty requests to `GET /students/` automatically have `StudentEnrollment.division_id.in_(allowed_divisions)` appended to the database query. Duplicate students resulting from multiple assignments to the same division are naturally prevented by standard SQLAlchemy joins. Requesting an invalid division throws a 403.

## 6. Student Detail Protection
`GET /students/{user_id}` validates that the student's active enrollment division matches the Faculty's allowed division scope. If not, it returns `404 Not Found` to prevent revealing the existence of unauthorized students.

## 7. Faculty API Protection
`GET /faculty/` (list all) and all mutations (create, edit, toggle status) remain strictly Admin-only. `GET /faculty/{user_id}` and `GET /faculty/{user_id}/subjects` allow Faculty access *only* if the requested `user_id` matches the authenticated JWT's `sub`. Otherwise, it returns 404.

## 8. Subject/Division Protection
When `FACULTY` calls `GET /academic/subjects` or `GET /academic/divisions`, the backend intercepts the query and filters it using `.filter(Subject.id.in_(allowed_subjects))` and `.filter(Division.id.in_(allowed_divisions))`. Unassigned subjects (e.g. Deep Learning for a DSA professor) are entirely hidden.

## 9. Assignment Protection
`POST /faculty/{user_id}/subjects` remains wrapped by `require_admin`. Faculty cannot create, modify, or delete their own assignments or assignments of others.

## 10. Admin Stats
`GET /api/v1/admin/stats/` is strictly guarded by `require_role(RoleName.ADMIN)`. Faculty attempts return HTTP 403.

## 11. Security Test Matrix
I built an automated FastAPI TestClient test script (`test_authorization.py`) that confirmed:
- **Test A:** Faculty Authorized Scope: PASS
- **Test B/C:** Faculty Unauthorized Division: PASS (403 returned)
- **Test D:** Faculty Unauthorized Student ID: PASS (404 returned)
- **Test E:** Faculty accessing /admin/stats: PASS (403 returned)
- **Test F/P:** Faculty mutate student: PASS (403 returned)
- **Test G/Q:** Faculty mutate assignment: PASS (403 returned)
- **Test H:** Admin access students: PASS (200 returned)
- **Test I:** Admin access stats: PASS (200 returned)
- **Test J:** Faculty manipulates division_id: PASS (403 returned)
- **Test K:** Faculty manipulates semester_id: PASS (403 returned)
- **Test L:** Faculty accessing other Faculty: PASS (404 returned)
- **Test M:** Faculty accesses unrelated subject: PASS (Filtered out)
- **Test N:** Faculty accesses unrelated division: PASS (Filtered out)

## 12. Admin Regression
The UI (`StudentsList.tsx` and `Dashboard.tsx`) remains unaffected as Admin requests skip the Faculty filtering and return all data correctly. 

## 13. Database Integrity
Confirmed via live SQL queries:
- Students = 360
- Faculty = 20
- Subjects = 60
- Divisions = 6
- StudentEnrollments = 360
- FacultySubjectAssignments = 46
- Attendance = 0
- AttendanceSessions = 0
- FaceTemplates = 0

## 14. Files Modified
- `backend/api/dependencies.py`: Added scope and role dependency helpers.
- `backend/api/routes/students.py`: Implemented query-level enforcement and admin-only mutation overrides.
- `backend/api/routes/faculty.py`: Self-only profile access for faculty; admin-only list/mutations.
- `backend/api/routes/academic.py`: Scoped subject/division visibility.
- `backend/api/routes/attendance.py`: Secured QR and Session fetching.

## 15. Problems / Issues
Initially, my automated test script failed Test E and I by targeting `/api/v1/stats/` directly, forgetting it was mounted via `api_router.include_router` as `/admin/stats/`. After correction, the endpoints behaved flawlessly.

## 16. Final Status
COMPLETE
