# Functional Requirements — SecureAttend AI

## FR-AUTH — Authentication & Authorization

| ID | Requirement | Role |
|----|-------------|------|
| FR-AUTH-01 | Users authenticate with username/email + password | ALL |
| FR-AUTH-02 | Login response includes access token, refresh token, expiration, user info, authoritative role | ALL |
| FR-AUTH-03 | Refresh token rotation with revocation on logout | ALL |
| FR-AUTH-04 | Account activation/deactivation by Admin | ADMIN |
| FR-AUTH-05 | Password reset by Admin for Student/Faculty | ADMIN |
| FR-AUTH-06 | Rate limiting on login and sensitive endpoints | ALL |
| FR-AUTH-07 | Backend RBAC on every protected endpoint | ALL |

## FR-ADMIN — Admin Web Portal

| ID | Requirement |
|----|-------------|
| FR-ADMIN-01 | Admin login, logout, session management |
| FR-ADMIN-02 | Dashboard with KPIs and analytics |
| FR-ADMIN-03 | Student CRUD, search, filter, pagination, deactivate/reactivate |
| FR-ADMIN-04 | Faculty CRUD, search, filter, pagination, deactivate/reactivate |
| FR-ADMIN-05 | Academic entity management (departments, years, semesters, divisions, subjects, classrooms) |
| FR-ADMIN-06 | Student enrollments and faculty subject assignments |
| FR-ADMIN-07 | Timetable management |
| FR-ADMIN-08 | Attendance session and record viewing |
| FR-ADMIN-09 | Manual attendance corrections with audit trail |
| FR-ADMIN-10 | Reports with CSV/Excel/PDF export |
| FR-ADMIN-11 | System settings (thresholds, QR interval, retention) |
| FR-ADMIN-12 | Audit log viewing |

## FR-FACE-ENROLL — Face Enrollment

| ID | Requirement |
|----|-------------|
| FR-FE-01 | Only Admin can initiate enrollment |
| FR-FE-02 | Browser webcam capture with live preview |
| FR-FE-03 | Guided pose sequence (straight, left, right, up, down) |
| FR-FE-04 | 5–10 validated samples per enrollment |
| FR-FE-05 | Per-sample quality validation (single face, size, blur, brightness, pose) |
| FR-FE-06 | Enrollment liveness check |
| FR-FE-07 | Embedding generation and consistency check |
| FR-FE-08 | Template stored as float32 BLOB with metadata |
| FR-FE-09 | Re-enrollment without deactivating old profile until success |
| FR-FE-10 | Audit events for enrollment actions |

## FR-STUDENT-MOBILE — Student Mobile (API only; UI by Antigravity)

| ID | Requirement |
|----|-------------|
| FR-SM-01 | Dashboard, today's schedule, attendance history/summary |
| FR-SM-02 | Liveness challenge request and completion |
| FR-SM-03 | Face verification with multipart image upload |
| FR-SM-04 | Short-lived face verification proof on success |
| FR-SM-05 | QR scan + proof submission for attendance marking |
| FR-SM-06 | Notifications list |
| FR-SM-07 | Profile via `/mobile/me` |

## FR-FACULTY-MOBILE — Faculty Mobile (API only; UI by Antigravity)

| ID | Requirement |
|----|-------------|
| FR-FM-01 | Dashboard, today's schedule, assigned subjects |
| FR-FM-02 | Create attendance session for authorized class |
| FR-FM-03 | Retrieve dynamic QR token for active session |
| FR-FM-04 | Live attendance, present list, absent list |
| FR-FM-05 | End attendance session |
| FR-FM-06 | Attendance history |

## FR-QR — Dynamic QR Authentication

| ID | Requirement |
|----|-------------|
| FR-QR-01 | Server generates cryptographically random session secret |
| FR-QR-02 | HMAC-signed QR tokens with epoch, expiry, nonce |
| FR-QR-03 | Default 15-second rotation interval |
| FR-QR-04 | Multiple students can scan same epoch token |
| FR-QR-05 | Validation logs for all attempts |

## FR-ATTEND — Secure Attendance Marking

| ID | Requirement |
|----|-------------|
| FR-AT-01 | Single authoritative marking endpoint |
| FR-AT-02 | Validates QR, face proof, liveness, enrollment, window |
| FR-AT-03 | UNIQUE(attendance_session_id, student_id) constraint |
| FR-AT-04 | Concurrent duplicate handling |
| FR-AT-05 | Attendance receipt on success |
| FR-AT-06 | AI inference before SQLite write transaction |

## FR-REPORT — Reports & Analytics

| ID | Requirement |
|----|-------------|
| FR-RP-01 | Daily, weekly, monthly reports |
| FR-RP-02 | Student, subject, faculty, department reports |
| FR-RP-03 | Low attendance report |
| FR-RP-04 | Export CSV, Excel, PDF |

## FR-AUDIT — Audit & Notifications

| ID | Requirement |
|----|-------------|
| FR-AU-01 | Immutable audit logs for security events |
| FR-AU-02 | In-app notifications for students |
| FR-AU-03 | Enrollment, verification, attendance audit trails |
