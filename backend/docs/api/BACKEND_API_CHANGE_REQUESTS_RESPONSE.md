# Backend API Change Requests — Response

**Date:** 2026-07-07  
**Reviewer:** Cursor (Backend Agent)  
**Source:** Antigravity `BACKEND_API_CHANGE_REQUESTS.md`

## Summary

All requested capabilities are **approved**. Several endpoint paths are **modified** to align with the authoritative API contract defined in the master development specification. One endpoint (`GET /api/v1/faculty/attendance-sessions/{session_id}/qr`) is **rejected** in favor of polling `GET .../qr`.

## Detailed Decisions

### 1. Authentication & Profile

| Request | Decision | Authoritative Endpoint |
|---------|----------|----------------------|
| `POST /auth/login` | **Approved** (path prefixed) | `POST /api/v1/auth/login` |
| `POST /auth/refresh` | **Approved** (path prefixed) | `POST /api/v1/auth/refresh` |
| `POST /auth/logout` | **Approved** (path prefixed) | `POST /api/v1/auth/logout` |
| `GET /api/v1/mobile/me` | **Modified** | `GET /api/v1/mobile/me` |

**Rationale for `/mobile/me`:** Single profile endpoint serves both STUDENT and FACULTY roles from one APK. Response includes authoritative `role` field for GoRouter guards. Avoids role-specific profile endpoints.

**Login response includes:**
- `access_token`, `refresh_token`
- `token_type`: "bearer"
- `expires_in`: seconds
- `user`: { id, username, email, role, profile }

### 2. Student Flow

| Request | Decision | Authoritative Endpoint |
|---------|----------|----------------------|
| `GET /student/schedule/today` | **Approved** | `GET /api/v1/student/schedule/today` |
| `GET /student/attendance/mark/summary` | **Approved** | `GET /api/v1/student/attendance/mark/summary` |
| `GET /student/attendance/mark/history` | **Approved** | `GET /api/v1/student/attendance/mark/history` |
| `GET /student/notifications` | **Approved** | `GET /api/v1/student/notifications` |
| `POST /api/v1/student/face-verification/challenge` | **Modified** | `POST /api/v1/student/face-verification/challenge` |
| `POST /api/v1/student/face-verification/verify` | **Modified** | `POST /api/v1/student/face-verification/verify` |
| `POST /api/v1/student/attendance/mark/mark` | **Modified** | `POST /api/v1/student/attendance/mark/mark` |

**Rationale for POST challenge:** Challenge creation stores server-side state (challenge_id, sequence, expiry). GET would be idempotent and cannot create state.

**Rationale for `/mark` suffix:** Distinguishes marking from history/summary endpoints. Explicit action naming.

**Face proof field name:** `face_verification_proof` (not `face_proof_token`) in attendance mark request.

### 3. Faculty Flow

| Request | Decision | Authoritative Endpoint |
|---------|----------|----------------------|
| `GET /faculty/schedule/today` | **Approved** | `GET /api/v1/faculty/schedule/today` |
| `GET /faculty/subjects` | **Approved** | `GET /api/v1/faculty/subjects` |
| `POST /api/v1/faculty/attendance-sessions` | **Modified** | `POST /api/v1/faculty/attendance-sessions` |
| `GET /api/v1/faculty/attendance-sessions/{session_id}` | **Modified** | `GET /api/v1/faculty/attendance-sessions/{session_id}` |
| `GET /api/v1/faculty/attendance-sessions/{session_id}/qr` | **Rejected** | Use `GET /api/v1/faculty/attendance-sessions/{session_id}/qr` |
| `GET /api/v1/faculty/attendance-sessions/{session_id}/live` | **Modified** | `GET .../live`, `.../present`, `.../absent` |
| `POST /api/v1/faculty/attendance-sessions/{session_id}/end` | **Modified** | `POST /api/v1/faculty/attendance-sessions/{session_id}/end` |

**Rationale for rejecting refresh-qr:**

Dynamic QR uses epoch-based rotation. Polling `GET .../qr` every ~12 seconds returns the current epoch token with `expires_at`. A separate refresh endpoint is redundant and introduces unnecessary state synchronization complexity.

**Faculty workflow change for Antigravity:**

1. `POST /faculty/attendance-sessions` with `{ "timetable_entry_id": 123 }` → returns `session_id`
2. Poll `GET /faculty/attendance-sessions/{session_id}/qr` for QR display
3. Poll `GET .../live` for attendance counts
4. `POST .../end` to terminate

**Additional approved endpoints not in original request:**
- `GET /api/v1/faculty/dashboard`
- `GET /api/v1/faculty/attendance-history`
- `GET /api/v1/student/dashboard`

## Security Review

All approved endpoints enforce:
- JWT authentication
- Backend RBAC
- Rate limiting on sensitive operations
- No client-provided role/identity trust

No security concerns block approval.

## Backward Compatibility

This is the initial contract (v0.1.0). No backward compatibility constraints yet.

## Action Items for Antigravity

1. Update API base URL pattern to `/api/v1`
2. Replace `/mobile/me` with `/mobile/me`
3. Replace face challenge GET with POST
4. Replace faculty session endpoints with RESTful attendance-sessions resource
5. Implement QR polling instead of refresh-qr POST
6. Map error codes from [ERROR_CODES.md](./ERROR_CODES.md)
7. Review [FLUTTER_INTEGRATION_GUIDE.md](./FLUTTER_INTEGRATION_GUIDE.md)

## Action Items for Cursor

1. Implement endpoints in Phases 2, 5, 6, 7
2. Export OpenAPI on each phase completion
3. Update this response if decisions change
