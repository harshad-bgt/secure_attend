# Contributing to SecureAttend AI

## Two-Agent Development Model

This repository is developed in coordination with a separate Flutter mobile application built by the Antigravity agent. The **REST API contract** in `docs/api/` is the shared integration boundary.

| Component | Owner |
|-----------|-------|
| FastAPI Backend, SQLite, AI Services, Admin Web Portal, API Contract | Cursor (this repo) |
| Flutter Android APK (Student + Faculty) | Antigravity |

## Development Rules

1. Work **phase-by-phase** as defined in the master development prompt.
2. Do not proceed to the next phase without explicit approval.
3. Never make **undocumented breaking API changes** to mobile endpoints.
4. Every mobile API change must update: implementation, tests, `API_SPECIFICATION.md`, `openapi.json`, `FLUTTER_INTEGRATION_GUIDE.md` (if needed), `ERROR_CODES.md`, `API_CHANGELOG.md`, and `DEVELOPMENT_PROGRESS.md`.

## API Change Workflow

When Antigravity submits requests via `BACKEND_API_CHANGE_REQUESTS.md`:

1. Review and document decision in `docs/api/BACKEND_API_CHANGE_REQUESTS_RESPONSE.md`.
2. Implement approved changes in the appropriate phase.
3. Update all contract documents.

## Code Standards

### Backend (Python)

- FastAPI, SQLAlchemy 2.0, Pydantic v2
- Type hints required
- Pytest for tests
- Run `ruff` / `mypy` when configured

### Admin Web (TypeScript)

- React, Vite, Tailwind, Shadcn UI
- Strict TypeScript
- Zod for form validation

## Security

- Never commit `.env`, secrets, database files, or raw biometric images.
- Never trust client-provided identity, role, or verification results.
- All protected endpoints must enforce backend authorization.

## Pull Requests

- Include tests for behavioral changes
- Update documentation
- Reference phase and issue if applicable
