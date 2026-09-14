# SECUREATTEND PHASE 6 — FINAL API FORENSIC DIAGNOSTIC

## 1. Faculty Identity
- **Logged-in user:** `faculty001@secureattend.demo`
- **Identity:** Prof. Neha Mahajan
- **User ID:** `364`
- **Role:** `FACULTY`

## 2. Database Assignment Records
The SQLite database `secureattend.db` contains exactly **3 assignments** for `faculty_id = 364`:
- Assignment 1: Subject ID 4 (Data Structures & Algorithms), Division ID 1 (Division A), Semester ID 1
- Assignment 27: Subject ID 27 (Program Elective-1), Division ID 3 (Division A), Semester ID 3
- Assignment 28: Subject ID 27 (Program Elective-1), Division ID 4 (Division B), Semester ID 3

## 3. Exact Browser Request (Simulated via Node/Axios)
- **URL:** `http://127.0.0.1:8000/api/v1/faculty/364/subjects`
- **Method:** `GET`
- **Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`

## 4. Exact HTTP Status
**Status:** `200 OK`

## 5. Exact API Response
```json
[
  {
    "assignment_id": 1,
    "subject_id": 4,
    "subject_name": "Data Structures & Algorithms",
    "subject_code": "N-PCCCM30IT",
    "division_id": 1,
    "division_name": "Division A"
  },
  {
    "assignment_id": 27,
    "subject_id": 27,
    "subject_name": "Program Elective-1",
    "subject_code": null,
    "division_id": 3,
    "division_name": "Division A"
  },
  {
    "assignment_id": 28,
    "subject_id": 27,
    "subject_name": "Program Elective-1",
    "subject_code": null,
    "division_id": 4,
    "division_name": "Division B"
  }
]
```

## 6. Backend Log/Error
- **FastAPI / Uvicorn Terminal:** No exceptions thrown. The endpoint completes successfully and returns the serialized JSON.

## 7. Frontend React Query State
- If the endpoint throws an HTTP error (e.g., 401, 500) or a Network Error (e.g., server offline), React Query catches the exception.
- `data` becomes `undefined`.
- The destructuring `const { data: assignments = [] } = useQuery(...)` defaults to an empty array `[]`.
- This masks the error and causes the UI to render `0` subjects and `0` divisions.

## 8. Response Schema
The backend returns a flat dictionary containing:
- `assignment_id`
- `subject_id`, `subject_name`, `subject_code`
- `division_id`, `division_name`
*(Crucially missing: `semester_id`)*

## 9. Frontend Expected Schema
- **FacultyDashboard.tsx / MySubjects.tsx:** Expects `subject_id`, `division_id`, `subject_name`, `subject_code`, `division_name`. (Matches backend perfectly).
- **MyStudents.tsx:** Expects `semester_id` (Requires `a.semester_id` to map to `SEMESTER_YEAR_MAP`). (Incompatible).

## 10. MySubjects Behavior
- Uses the same `GET /faculty/{user_id}/subjects` endpoint.
- If React Query successfully fetches the array, it renders the 3 subject cards correctly because it relies on the same flat fields.

## 11. MyProfile Behavior
- Uses `GET /auth/me`.
- Works successfully, returning `{"id":364, "first_name":"Neha", "last_name":"Mahajan", ...}`.

## 12. MyStudents Behavior
- Relies on the same `GET /faculty/{user_id}/subjects` endpoint.
- **Critical Failure:** It executes `const year = SEMESTER_YEAR_MAP[a.semester_id];`. Because `semester_id` is entirely missing from the backend response, `year` is undefined. 
- The assignment scope fails to build, and it renders: *"No students are currently within your assignment scope."*

## 13. Exact Root-Cause Category A-I
**Category H (API returns invalid/incompatible response schema)**
- **Evidence:** The backend response definitively misses `semester_id`, which explicitly breaks the core logic in `MyStudents.tsx`.
- *Note on FacultyDashboard showing 0:* Because the direct runtime test proves the backend returns `200 OK` with valid data that matches `FacultyDashboard.tsx` expectations, the UI rendering `0` in the user's screenshot indicates either a transient Network Error (server crash immediately prior to the request), an expired token (401), or a React Query cache failure that returned `undefined`, which destructured to `[]`. The API itself is fully functional and does not return 500 or an empty array.

## 14. Minimal Recommended Fix
Update the backend serialization logic in `get_faculty_subjects` to include `semester_id` from the `FacultySubjectAssignment` record.

## 15. Files that would need modification
- `backend/api/routes/faculty.py` (Lines 159-170)
