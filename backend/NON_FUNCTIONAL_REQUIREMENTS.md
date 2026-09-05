# Non-Functional Requirements — SecureAttend AI

## NFR-PERF — Performance

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-PERF-01 | Face detection + embedding on laptop CPU | < 2s per frame |
| NFR-PERF-02 | Attendance marking API (excl. client upload) | < 500ms p95 |
| NFR-PERF-03 | QR validation | < 50ms |
| NFR-PERF-04 | Admin dashboard load | < 3s on demo dataset |
| NFR-PERF-05 | SQLite write transactions for attendance | < 100ms |

## NFR-SEC — Security

| ID | Requirement |
|----|-------------|
| NFR-SEC-01 | Argon2 password hashing |
| NFR-SEC-02 | Short-lived JWT access tokens (15 min default) |
| NFR-SEC-03 | Refresh token rotation and revocation |
| NFR-SEC-04 | Never trust client-provided role, identity, or verification flags |
| NFR-SEC-05 | Face proof bound to user, event, purpose, expiry |
| NFR-SEC-06 | QR tokens never expose raw session secret |
| NFR-SEC-07 | Rate limiting on auth and attendance endpoints |
| NFR-SEC-08 | CORS restricted to known origins (no wildcard in production) |
| NFR-SEC-09 | Audit logging for sensitive operations |

## NFR-REL — Reliability

| ID | Requirement |
|----|-------------|
| NFR-REL-01 | SQLite WAL mode with busy timeout |
| NFR-REL-02 | Idempotent duplicate attendance rejection |
| NFR-REL-03 | Safe concurrent attendance marking |
| NFR-REL-04 | Graceful degradation when AI model unavailable |

## NFR-SCALE — Scalability (Academic Scope)

| ID | Requirement |
|----|-------------|
| NFR-SCL-01 | Support ~500 students, ~50 faculty for demo |
| NFR-SCL-02 | ~60 concurrent attendance marks per session |
| NFR-SCL-03 | ORM models portable to PostgreSQL for future migration |

## NFR-UX — Usability

| ID | Requirement |
|----|-------------|
| NFR-UX-01 | Admin portal responsive on laptop screens |
| NFR-UX-02 | Mobile API returns structured, actionable error codes |
| NFR-UX-03 | Face enrollment guided instructions in Admin UI |

## NFR-OPS — Operability

| ID | Requirement |
|----|-------------|
| NFR-OPS-01 | Single-command local network startup |
| NFR-OPS-02 | Health check endpoint |
| NFR-OPS-03 | Environment-based configuration via `.env` |
| NFR-OPS-04 | Documented LAN IP discovery and firewall setup |

## NFR-MAINT — Maintainability

| ID | Requirement |
|----|-------------|
| NFR-MNT-01 | Modular AI service adapters (replaceable models) |
| NFR-MNT-02 | OpenAPI-documented API contract |
| NFR-MNT-03 | Phase-by-phase development with completion reports |
| NFR-MNT-04 | Pytest coverage for critical paths |

## NFR-PRIV — Privacy

| ID | Requirement |
|----|-------------|
| NFR-PRV-01 | No permanent raw face image storage by default |
| NFR-PRV-02 | Embeddings stored as opaque BLOBs, not pickle |
| NFR-PRV-03 | Configurable biometric retention policy |
| NFR-PRV-04 | Face profile deletion per privacy policy |

## NFR-COMPAT — Compatibility

| ID | Requirement |
|----|-------------|
| NFR-CMP-01 | Python 3.11+ |
| NFR-CMP-02 | Node.js 20+ for Admin Portal |
| NFR-CMP-03 | Android 8+ for Flutter APK |
| NFR-CMP-04 | Chrome/Edge/Firefox for Admin Portal webcam |

## NFR-DOC — Documentation

| ID | Requirement |
|----|-------------|
| NFR-DOC-01 | Complete API specification for Flutter team |
| NFR-DOC-02 | Architecture and threat model documents |
| NFR-DOC-03 | Local network deployment guide |
| NFR-DOC-04 | API changelog for contract changes |
