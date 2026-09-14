# SecureAttend Phase 7 — Implementation Plan

This document outlines the discovery findings and implementation steps for Phase 7 (Attendance Workflow). The core objective of Phase 7 is to activate the operational attendance pipeline using the infrastructure and foundations built in Phases 1–6.

## 1. Current Architecture
- **Backend**: FastAPI with SQLAlchemy (SQLite). Contains established JWT-based authentication and Role-Based Access Control (RBAC).
- **Frontend**: React (Vite, TypeScript, Tailwind) Admin and Faculty panels.
- **Mobile**: Flutter APK for Students.
- **Biometrics**: InsightFace (`buffalo_l` model) implemented in `services/face_service.py` via ONNX runtime on CPU.

## 2. Existing Attendance Capabilities
The database schema (`backend/api/models.py`) already contains fully formed models for Phase 7:
- `AttendanceSession`: Tracks `faculty_id`, `subject_id`, `division_id`, `start_time`, `end_time`, `is_active`, `current_qr_token`, `qr_expires_at`.
- `AttendanceRecord`: Tracks `attendance_session_id`, `student_id`, `marked_at`, `status`.

**Conclusion**: **REUSE EXISTING**. The database schema fully supports the Phase 7 lifecycle without modification.

## 3. Existing QR Capabilities
Dynamic QR functionality is already implemented in the backend:
- `create_attendance_qr_token()` in `security.py` generates a signed JWT containing the `session_id` and a strict 60-second expiration.
- `GET /attendance-sessions/{session_id}/qr` automatically issues or rotates the QR token when expired, securely fetching it via DB locks (`with_for_update`).
- `verify_attendance_qr_token()` enforces server-side validation of token expiry and authenticity.

**Conclusion**: **REUSE EXISTING**. No new QR architecture is needed.

## 4. Existing Face Capabilities
InsightFace functionality is already robustly integrated:
- `POST /student/face-enrollment/enroll` accepts an image, extracts embeddings, and saves it to `FaceTemplate`.
- `POST /student/face-verification/verify` validates incoming frames against enrolled embeddings at a strict `0.40` threshold.
- Successful verification yields a 60-second `face_proof_token` (JWT) to securely transition state to the attendance submission without replay vulnerabilities.

**Conclusion**: **REUSE EXISTING**. The biometric engine requires no modification.

## 5. Existing Student APK Capabilities
The Flutter source tree (`apk_build/lib/screens/`) already contains:
- `student_qr_scanner.dart`
- `student_face_enrollment.dart`
- `student_face_verification.dart`

**Conclusion**: **REUSE EXISTING**. The student flow logic exists, requiring only minor routing orchestration to link the scanner, face verification, and submission into a seamless pipeline.

## 6. Existing Faculty Capabilities
The `backend/admin/src/pages/attendance/` directory contains highly functional prototypes (`LiveSessionView.tsx`, `StartSessionDialog.tsx`) developed previously. However, the Faculty Web Panel (`faculty-panel`) from Phase 6 does not yet expose this UI.

**Conclusion**: **NEW REQUIRED (UI Orchestration)**. We need to integrate the existing `LiveSessionView` into the `FacultyDashboard` context.

## 7. Database Support & Duplicate Prevention
- `AttendanceRecord` has a `UniqueConstraint('attendance_session_id', 'student_id', name='uix_session_student_attendance')`.
- The `POST /student/attendance/mark` endpoint catches this explicitly and returns a `409 Conflict`.

**Conclusion**: **REUSE EXISTING**. Duplicate attendance is securely prevented at both the application and database tiers.

## 8. APIs That Can Be Reused
The following endpoints in `attendance.py` and `student_attendance.py` perfectly fulfill Phase 7:
- `POST /attendance-sessions` (Start Session)
- `POST /attendance-sessions/{session_id}/end` (End Session)
- `GET /attendance-sessions/active` (Poll active sessions)
- `GET /attendance-sessions/{session_id}/qr` (Poll live QR)
- `GET /attendance-sessions/{session_id}/attendance` (Poll live attendance)
- `POST /student/face-enrollment/enroll`
- `POST /student/face-verification/verify`
- `POST /student/attendance/mark`

**Conclusion**: All core APIs are ready.

## 9. APIs That Must Be Added
**NONE**. The existing API contracts cover 100% of Phase 7's requirements.

## 10. Backend Changes
- **Minor Fixes only**: Ensure endpoint paths perfectly align with the frontend API client. For instance, `LiveSessionPage.tsx` currently queries `/admin/attendance-sessions/active` which should likely be `/attendance-sessions/active`.
- Ensure CORS and permission dependencies (`get_faculty_scopes`) are firing smoothly for these routes.

## 11. Faculty Web Changes
**Expected File Changes**:
1. `backend/admin/src/pages/faculty-panel/FacultyDashboard.tsx`
   - Add a "Start Session" button linking to a dialog or page.
2. `backend/admin/src/pages/faculty-panel/FacultyLiveSession.tsx` **[NEW]**
   - Create a dedicated view combining the live QR poller (`LiveSessionView.tsx` logic) and live attendance table.
3. `backend/admin/src/App.tsx`
   - Register the new `/faculty-panel/live-session` route.

## 12. Flutter Changes
**Expected Changes**:
- Ensure `student_qr_scanner.dart` extracts the `session_id` and forwards it sequentially to `student_face_verification.dart`.
- Upon successful face verification (receiving the `face_proof_token`), execute `POST /student/attendance/mark` supplying both the `qr_token` and `face_proof_token`.

## 13. Security Model
- **Faculty Scopes**: `get_faculty_scopes` ensures faculty cannot create sessions for subjects they don't teach.
- **Token Dual-Lock**: Attendance submission is dual-locked. It requires a live, unexpired `qr_token` (proving they are physically present at the active session) AND an unexpired `face_proof_token` (proving biometric identity).
- **Session State**: Validations reject submissions against `is_active=False` sessions.

## 14. Session Lifecycle & Live Attendance Strategy
- **Lifecycle**: `CREATED (is_active=True)` -> `ACTIVE (Polling QR)` -> `ENDED (is_active=False)`.
- **Live Strategy**: We will utilize **React Query Polling** (`refetchInterval: 3000`) on `GET /attendance-sessions/{id}/attendance` for the Faculty web panel. WebSockets are explicitly not required, keeping the architecture simple and aligned with existing code.

## 15. Testing & Data Integrity Strategy
- Validate no schema alterations occurred (`Students=360`, `Faculty=20`, `Subjects=60`, etc).
- Verify a Faculty cannot start a session for an unauthorized Division.
- Verify Student QR replay fails after 60 seconds.
- Verify Student face replay fails (invalid `face_proof_token`).

## 16. Recommended Implementation Order
1. Implement Faculty Web routing (`FacultyLiveSession.tsx` and `StartSessionDialog`).
2. Verify Faculty can successfully create, view live QR, and end a session.
3. Wire the Flutter Student sequential workflow (Scan -> Verify -> Submit).
4. Perform end-to-end testing with a test student enrollment.
