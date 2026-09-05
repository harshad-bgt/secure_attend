# Backend API Change Requests

## CRITICAL: Complete API Contract Missing
**Blocking Development Phase**: Phase 8 (Full Integration), Phase 1-7 require mocks if development proceeds before the contract is available.
**Reason**: No `openapi.json`, `API_SPECIFICATION.md`, or any API documentation exists in the repository. The Cursor agent has not yet generated the shared API contract.

To support the mobile requirements defined in Phase 0, the following endpoints MUST be included in the API contract. **Do not invent these on the mobile side.**

### 1. Authentication & Profile
- **Mobile Feature**: Login, Token Storage, Refresh, Logout, Role parsing.
- **Required Endpoint**: `POST /auth/login` (Returns access_token, refresh_token, user_role, profile_data)
- **Required Endpoint**: `POST /auth/refresh` (Accepts refresh token, returns new access token)
- **Required Endpoint**: `POST /auth/logout` (Invalidates tokens on backend)
- **Required Endpoint**: `GET /api/v1/mobile/me` (Returns current user profile and role)

### 2. Student Flow
- **Mobile Feature**: Student Dashboard & Schedule
- **Required Endpoint**: `GET /student/schedule/today`
- **Required Endpoint**: `GET /student/attendance/mark/summary`
- **Required Endpoint**: `GET /student/attendance/mark/history`
- **Required Endpoint**: `GET /student/notifications`

- **Mobile Feature**: Student Liveness & Face Verification
- **Required Endpoint**: `POST /api/v1/student/face-verification/challenge` (Returns liveness instructions e.g., `["look_straight"]`)
- **Required Endpoint**: `POST /api/v1/student/face-verification/verify` (Multipart upload for liveness media. Returns short-lived `face_proof_token`)

- **Mobile Feature**: Dynamic QR Scan & Attendance Submission
- **Required Endpoint**: `POST /api/v1/student/attendance/mark/mark` (Accepts `qr_token` from scan + `face_proof_token` from verification)

### 3. Faculty Flow
- **Mobile Feature**: Faculty Dashboard & Schedule
- **Required Endpoint**: `GET /faculty/schedule/today`
- **Required Endpoint**: `GET /faculty/subjects`

- **Mobile Feature**: Attendance Session Management & Dynamic QR
- **Required Endpoint**: `POST /api/v1/faculty/attendance-sessions` (Starts session for a specific class schedule ID)
- **Required Endpoint**: `GET /api/v1/faculty/attendance-sessions/{session_id}` (Returns active session data including current `qr_token` and `expires_at` timestamp)
- **Required Endpoint**: `GET /api/v1/faculty/attendance-sessions/{session_id}/qr` (Manually or auto-triggered to get the next time-limited QR string)
- **Required Endpoint**: `GET /api/v1/faculty/attendance-sessions/{session_id}/live` (Polls for current present/absent student list)
- **Required Endpoint**: `POST /api/v1/faculty/attendance-sessions/{session_id}/end` (Terminates the active session)

*Note: All endpoints above require proper error code mapping as defined in the architectural guidelines.*
