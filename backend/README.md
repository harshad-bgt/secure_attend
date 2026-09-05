# SecureAttend AI

**AI-Based Multi-Factor Smart Attendance Management System** using Face Verification, Liveness Detection, Dynamic QR Authentication, and Role-Based Access Control.

## Overview

SecureAttend AI is an academic smart attendance system designed for local-network deployment on a laptop, with Android mobile clients connecting over Wi-Fi.

| Component | Technology | Users |
|-----------|------------|-------|
| Admin Web Portal | React, TypeScript, Vite | ADMIN only |
| Backend API | FastAPI, Python, SQLite | All roles |
| Mobile App | Flutter APK (separate repo) | STUDENT, FACULTY |

## Repository Structure

```
backend/
├── apps/admin-web/          # React Admin Portal (Phase 1+)
├── backend/                 # FastAPI application (Phase 1+)
├── ml/                      # Face and liveness model adapters (Phase 4+)
├── migrations/              # Alembic migrations (Phase 2+)
├── tests/                   # Backend and contract tests
├── data/                    # SQLite DB (gitignored)
├── docs/                    # Architecture, API contract, security
└── scripts/                 # Local network startup scripts
```

## Current Status

**Phase 0 — Complete** (Architecture and API Contract)

See [DEVELOPMENT_PROGRESS.md](./DEVELOPMENT_PROGRESS.md) for the full roadmap.

## Quick Links

| Document | Description |
|----------|-------------|
| [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) | Project summary |
| [docs/architecture/SYSTEM_ARCHITECTURE.md](./docs/architecture/SYSTEM_ARCHITECTURE.md) | System design |
| [docs/api/API_SPECIFICATION.md](./docs/api/API_SPECIFICATION.md) | REST API contract |
| [docs/api/FLUTTER_INTEGRATION_GUIDE.md](./docs/api/FLUTTER_INTEGRATION_GUIDE.md) | Mobile integration guide |
| [docs/api/openapi.json](./docs/api/openapi.json) | OpenAPI 3.1 skeleton |
| [docs/architecture/LOCAL_NETWORK_DEPLOYMENT.md](./docs/architecture/LOCAL_NETWORK_DEPLOYMENT.md) | LAN deployment |

## Roles

- **ADMIN** — Uses Admin Web Portal only
- **FACULTY** — Uses Flutter APK; manages attendance sessions
- **STUDENT** — Uses Flutter APK; marks attendance via face + QR

The backend returns the authoritative role at login. Users never select roles manually.

## Mobile Integration

The Flutter application is developed separately by Antigravity. Integration is via the REST API contract in `docs/api/`. Do not use `localhost` from physical Android devices — use the laptop's LAN IP address.

## License

MIT — see [LICENSE](./LICENSE).
