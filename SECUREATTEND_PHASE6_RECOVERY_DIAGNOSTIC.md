# Phase 6 Recovery Diagnostic Report

## 1. Identity Verification
- **Frontend Identity**: The `FacultyDashboard.tsx` component relies on the `AuthContext` to provide the `user` object. The `/auth/me` endpoint populates this object by returning the logged-in user's primary key as `id` (e.g., `id: 364` for Prof. Mahajan). 
- **Backend Expected Identity**: The API endpoint `GET /faculty/{user_id}/subjects` explicitly defines the path parameter `user_id: int`. It then queries `FacultySubjectAssignment.faculty_id == user_id`.
- **Database Schema Match**: The `faculty_subject_assignments` table defines `faculty_id` as a foreign key to `faculty.user_id`, which in turn is a foreign key to `users.id`. 
- **Conclusion**: There is **no identity mismatch**. The frontend passes the `users.id` (364), and the backend expects the `users.id` (364). The database stores the `users.id` (364).

## 2. API Endpoint Analysis
- **Route Definition**: The route `@router.get("/{user_id}/subjects")` is correctly defined in `routes/faculty.py` and is correctly nested under the `/faculty` prefix in `main.py`. It is not shadowed by any other routes.
- **Access Control**: The endpoint is guarded by `require_admin_or_faculty()`. Because the user is successfully authenticated as a Faculty member, this dependency passes. The endpoint further checks `if current_user.role.name == RoleName.FACULTY and user_id != current_user.id:`. Since both are exactly `364`, this check safely passes and does not raise a 404.
- **Database Query**: The query `db.query(FacultySubjectAssignment).filter(FacultySubjectAssignment.faculty_id == user_id).all()` is syntactically sound and executed against the `secureattend.db` database, which I verified contains exactly 3 assignments for `faculty_id = 364`.

## 3. Frontend Component Analysis
- **React Query**: `FacultyDashboard.tsx` makes the request using `await apiClient.get('/faculty/${user?.id}/subjects')`. React Query correctly waits for `user?.id` to be truthy before firing.
- **Response Mapping**: The backend serializes the result into a standard JSON array. Axios unwraps this into `.data`. React Query assigns this array to `assignments`. The component destructures this with a default of `[]` (`data: assignments = []`).
- **Data Rendering**: The component accurately checks `assignments.length > 0` and calculates unique subjects via `assignments.map((a: any) => a.subject_id)`.

## 4. Diagnostic Conclusion
If the frontend renders `My Subjects: 0` and `No active assignments found.`, it means the `assignments` array is strictly `[]`. Since the database absolutely contains 3 valid rows, this implies the API call is failing and throwing an exception (such as a 500 Internal Server Error), prompting React Query to fall back to the default `[]` array. 

This is not a logical mismatch in the IDs, but rather a runtime exception likely originating from the backend returning a 500 error or similar failure state during the API request, which React Query swallows and defaults to an empty array.
