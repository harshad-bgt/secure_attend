# SecureAttend AI Project Rules

## 1. Coding Standards
### Python (FastAPI Backend)
- **Format/Lint**: Use `black` and `ruff`.
- **Type Hinting**: All functions must have type hints. Use Pydantic strictly for input validation.
- **Async**: Use `async def` for I/O bound operations (DB, AI calls if offloaded).
- **Naming**: `snake_case` for variables/functions, `PascalCase` for Classes.

### TypeScript (React Admin)
- **Format/Lint**: Use `Prettier` and `ESLint` (Strict mode).
- **Components**: Functional components only with React Hooks.
- **State**: Use React Context for global state, or local state where sufficient.
- **Naming**: `camelCase` for variables/functions, `PascalCase` for Components/Interfaces.

### Dart (Flutter Mobile)
- **Format/Lint**: Use `dart format` and `flutter analyze`.
- **Architecture**: Riverpod for state management. GoRouter for navigation.
- **Naming**: `camelCase` for variables, `PascalCase` for Classes.
- **Widgets**: Extract widgets into separate files if they exceed 100 lines.

### SQLite Database
- **Migrations**: Alembic must be used for all schema changes. Never modify the schema directly.
- **Foreign Keys**: Enforce foreign keys (`PRAGMA foreign_keys = ON`).

## 2. API Design & REST Rules
- Follow OpenAPI 3.0 standards.
- Routes should be nouns (e.g., `/student/attendance/mark` not `/student/mark_attendance`).
- Always return consistent error formats.
- Version all APIs (e.g., `/api/v1/`).

## 3. Logging & Monitoring
- Do not log sensitive data (passwords, tokens, biometric payloads, QR tokens).
- Use structured logging (JSON) in production for the backend.

## 4. Git Workflow
- Branch naming: `feature/short-description`, `bugfix/issue-name`.
- Commit messages: Use imperative mood ("Add login endpoint" not "Added login endpoint").
- No direct commits to `main` without testing.

## 5. Documentation
- Synchronize `openapi.json` and `API_SPECIFICATION.md` with every backend change.
- Keep `DEVELOPMENT_PROGRESS.md` updated at the end of every phase.
- Use Mermaid diagrams for complex logic explanations.
