# Mobile API Coverage Matrix — SecureAttend AI

Tracks backend API readiness for each Antigravity mobile feature.

| Mobile Feature | Agent | Required Endpoint | Method | Role | Implementation Status | API Contract Status | Test Status | Antigravity Integration Status |
|----------------|-------|-------------------|--------|------|----------------------|--------------------|-------------|-------------------------------|
| Login | Antigravity | `/api/v1/auth/login` | POST | ALL | Not Started (Phase 2) | Defined v0.1.0 | Not Started | Not Started |
| Token Refresh | Antigravity | `/api/v1/auth/refresh` | POST | ALL | Not Started (Phase 2) | Defined v0.1.0 | Not Started | Not Started |
| Logout | Antigravity | `/api/v1/auth/logout` | POST | ALL | Not Started (Phase 2) | Defined v0.1.0 | Not Started | Not Started |
| Profile / Role | Antigravity | `/api/v1/mobile/me` | GET | STUDENT, FACULTY | Not Started (Phase 2) | Defined v0.1.0 | Not Started | Not Started |
| Student Dashboard | Antigravity | `/api/v1/student/dashboard` | GET | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| Student Schedule | Antigravity | `/api/v1/student/schedule/today` | GET | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| Attendance History | Antigravity | `/api/v1/student/attendance/mark/history` | GET | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| Attendance Summary | Antigravity | `/api/v1/student/attendance/mark/summary` | GET | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| Notifications | Antigravity | `/api/v1/student/notifications` | GET | STUDENT | Not Started (Phase 8) | Defined v0.1.0 | Not Started | Not Started |
| Liveness Challenge | Antigravity | `/api/v1/student/face-verification/challenge` | POST | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| Face Verification | Antigravity | `/api/v1/student/face-verification/verify` | POST | STUDENT | Not Started (Phase 5) | Defined v0.1.0 | Not Started | Not Started |
| QR Scan + Mark Attendance | Antigravity | `/api/v1/student/attendance/mark/mark` | POST | STUDENT | Not Started (Phase 7) | Defined v0.1.0 | Not Started | Not Started |
| Faculty Dashboard | Antigravity | `/api/v1/faculty/dashboard` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Faculty Schedule | Antigravity | `/api/v1/faculty/schedule/today` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Faculty Subjects | Antigravity | `/api/v1/faculty/subjects` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Start Session | Antigravity | `/api/v1/faculty/attendance-sessions` | POST | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Session Details | Antigravity | `/api/v1/faculty/attendance-sessions/{id}` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Dynamic QR Display | Antigravity | `/api/v1/faculty/attendance-sessions/{id}/qr` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Live Attendance Count | Antigravity | `/api/v1/faculty/attendance-sessions/{id}/live` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Present Students | Antigravity | `/api/v1/faculty/attendance-sessions/{id}/present` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Absent Students | Antigravity | `/api/v1/faculty/attendance-sessions/{id}/absent` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| End Session | Antigravity | `/api/v1/faculty/attendance-sessions/{id}/end` | POST | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Faculty History | Antigravity | `/api/v1/faculty/attendance-history` | GET | FACULTY | Not Started (Phase 6) | Defined v0.1.0 | Not Started | Not Started |
| Health Check | Both | `/api/v1/health` | GET | Public | Not Started (Phase 1) | Defined v0.1.0 | Not Started | Not Started |

## Status Legend

| Status | Meaning |
|--------|---------|
| Not Started | Phase not yet implemented |
| In Progress | Currently being implemented |
| Implemented | Backend code complete |
| Defined v0.1.0 | API contract documented in Phase 0 |
| Verified | Integration tested with physical device |

## Update Policy

Update this matrix when:
- Backend implementation completes for an endpoint
- API contract changes
- Tests pass
- Antigravity confirms mobile integration (only then mark Integration Status complete)

## Notes

- Antigravity Integration Status must **never** be marked complete without real mobile integration verification.
- Flutter team should use mocks until Phase 2+ backend endpoints are available.
- See [FLUTTER_INTEGRATION_GUIDE.md](./FLUTTER_INTEGRATION_GUIDE.md) for integration details.
