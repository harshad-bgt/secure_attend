# Requirements — SecureAttend AI

This document summarizes project requirements. Detailed breakdowns are in:

- [FUNCTIONAL_REQUIREMENTS.md](./FUNCTIONAL_REQUIREMENTS.md)
- [NON_FUNCTIONAL_REQUIREMENTS.md](./NON_FUNCTIONAL_REQUIREMENTS.md)

## Stakeholders

| Stakeholder | Interaction |
|-------------|-------------|
| System Administrator (ADMIN) | Admin Web Portal |
| Faculty | Flutter APK |
| Student | Flutter APK |
| Antigravity (Mobile Agent) | Consumes REST API contract |
| Cursor (Backend Agent) | Owns API contract and backend |

## High-Level Requirements

### R1 — Authentication

Single auth system for all roles. Login returns authoritative role. JWT access + refresh with rotation.

### R2 — Role-Based Access

Three roles: ADMIN, FACULTY, STUDENT. Backend authorization on every protected endpoint.

### R3 — Admin Portal

Full CRUD for students, faculty, academic entities, attendance management, reports, settings, audit logs.

### R4 — Face Enrollment

Admin-only, laptop webcam, guided multi-pose capture, template storage as float32 BLOB.

### R5 — Mobile Student Attendance

Liveness challenge → face verification → face proof → QR scan → attendance marking.

### R6 — Mobile Faculty Sessions

Start session → display dynamic QR → live attendance → end session.

### R7 — Dynamic QR

Server-side HMAC tokens, 15-second rotation, multi-student scan support.

### R8 — API Contract

Stable documented REST API for Flutter integration with machine-readable error codes.

### R9 — Local Network

Backend accessible from Android devices on same network. Documented deployment guide.

### R10 — SQLite

Primary database with WAL, FK enforcement, transactional attendance marking.

## Out of Scope (Initial Release)

- PostgreSQL / Redis / Celery
- Cloud deployment
- Student self-registration
- Student self-enrollment
- Production-grade anti-spoof liveness
- GPS / geofencing
- Separate Student and Faculty APKs

## Traceability

Each functional requirement maps to a development phase (0–10) in the master development prompt and is tracked in [DEVELOPMENT_PROGRESS.md](./DEVELOPMENT_PROGRESS.md).
