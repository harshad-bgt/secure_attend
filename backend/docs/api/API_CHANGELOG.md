# API Changelog — SecureAttend AI

All changes to the mobile API contract are recorded here. Antigravity must review this before integration phases.

Format: [Keep a Changelog](https://keepachangelog.com/) adapted for API contract versioning.

## [0.1.0] - 2026-07-07 — Phase 0 Initial Contract

### Added

Initial API contract skeleton (no backend implementation yet).

#### Authentication
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`

#### Mobile Profile
- `GET /api/v1/mobile/me`

#### Student Mobile
- `GET /api/v1/student/dashboard`
- `GET /api/v1/student/schedule/today`
- `GET /api/v1/student/attendance/mark/history`
- `GET /api/v1/student/attendance/mark/summary`
- `POST /api/v1/student/face-verification/challenge`
- `POST /api/v1/student/face-verification/verify`
- `POST /api/v1/student/attendance/mark/mark`
- `GET /api/v1/student/notifications`

#### Faculty Mobile
- `GET /api/v1/faculty/dashboard`
- `GET /api/v1/faculty/schedule/today`
- `GET /api/v1/faculty/subjects`
- `POST /api/v1/faculty/attendance-sessions`
- `GET /api/v1/faculty/attendance-sessions/{session_id}`
- `GET /api/v1/faculty/attendance-sessions/{session_id}/qr`
- `GET /api/v1/faculty/attendance-sessions/{session_id}/live`
- `GET /api/v1/faculty/attendance-sessions/{session_id}/present`
- `GET /api/v1/faculty/attendance-sessions/{session_id}/absent`
- `POST /api/v1/faculty/attendance-sessions/{session_id}/end`
- `GET /api/v1/faculty/attendance-history`

#### System
- `GET /api/v1/health`

### Contract Decisions (vs Antigravity Change Requests)

| Antigravity Request | Cursor Decision | Notes |
|--------------------|-----------------|-------|
| `GET /api/v1/mobile/me` | **Modified** → `GET /mobile/me` | Shared profile endpoint for both roles |
| `POST /api/v1/student/face-verification/challenge` | **Modified** → `POST /student/face-verification/challenge` | POST creates server-side challenge state |
| `POST /api/v1/student/face-verification/verify` | **Modified** → `POST /student/face-verification/verify` | Consistent namespace |
| `POST /api/v1/student/attendance/mark/mark` | **Modified** → `POST /api/v1/student/attendance/mark/mark/mark` | Explicit action |
| `POST /api/v1/faculty/attendance-sessions` | **Modified** → `POST /faculty/attendance-sessions` | RESTful resource creation |
| `GET /api/v1/faculty/attendance-sessions/{session_id}` | **Modified** → `GET /faculty/attendance-sessions/{id}` | Session ID from create response |
| `GET /api/v1/faculty/attendance-sessions/{session_id}/qr` | **Rejected** → use `GET .../qr` polling | QR refresh via epoch polling, no separate endpoint |
| `GET /api/v1/faculty/attendance-sessions/{session_id}/live` | **Modified** → `GET .../live`, `.../present`, `.../absent` | Granular endpoints |

See [BACKEND_API_CHANGE_REQUESTS_RESPONSE.md](./BACKEND_API_CHANGE_REQUESTS_RESPONSE.md) for full rationale.

### Error Codes

Initial stable error code registry in [ERROR_CODES.md](./ERROR_CODES.md).

### OpenAPI

Initial skeleton exported to [openapi.json](./openapi.json).

---

## Upcoming (Planned Phases)

| Phase | Expected Changes |
|-------|-----------------|
| Phase 2 | Auth endpoints implemented; schemas finalized |
| Phase 5 | Student mobile endpoints implemented |
| Phase 6 | Faculty session endpoints implemented |
| Phase 7 | Attendance marking implemented |
| Phase 8 | Notifications populated |

Breaking changes after Phase 0 require migration notes in this file.
