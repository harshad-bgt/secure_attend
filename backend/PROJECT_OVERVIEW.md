# Project Overview — SecureAttend AI

## Title

AI-Based Multi-Factor Smart Attendance Management System Using Face Verification, Liveness Detection, Dynamic QR Authentication, and Role-Based Access Control.

## Purpose

SecureAttend AI replaces manual or easily spoofed attendance methods with a multi-factor verification pipeline suitable for academic demonstration on consumer hardware over a local network.

## Problem Statement

Traditional attendance systems suffer from:

- Proxy attendance (one student marking for another)
- Manual roll-call inefficiency
- Lack of audit trails
- Weak identity verification

## Solution

A three-tier system where:

1. **Admin** enrolls students and manages academic data via a web portal with laptop webcam face enrollment.
2. **Faculty** starts attendance sessions displaying rotating dynamic QR codes via the mobile app.
3. **Students** mark attendance by completing liveness + face verification, then scanning the session QR.

## Deployment Model

Initial deployment targets a **local network**:

- Laptop runs Admin Portal + FastAPI + SQLite + AI inference
- Android phones connect via Wi-Fi/hotspot using the laptop's LAN IP
- Backend binds to `0.0.0.0:8000`

## Development Model

| Agent | Responsibility |
|-------|----------------|
| **Cursor** (this repo) | Backend, Admin Portal, SQLite, AI services, API contract |
| **Antigravity** (Flutter repo) | Single APK for Student + Faculty mobile UX |

The REST API contract in `docs/api/` is the authoritative integration boundary.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| RBAC | ADMIN, FACULTY, STUDENT with backend-enforced authorization |
| Face Enrollment | Admin-controlled webcam capture with guided poses |
| Face Verification | 1:1 match against enrolled template at attendance time |
| Liveness | Challenge-response (blink, head turn) — academic-grade, not production anti-spoof |
| Dynamic QR | HMAC-signed rotating tokens per attendance session |
| Secure Marking | Transactional attendance with duplicate prevention |
| Reports | Daily/weekly/monthly analytics with export |
| Audit | Immutable logs for security-sensitive operations |

## Known Limitations

The system does **not** use GPS, geofencing, BLE, or Wi-Fi proximity. Dynamic QR + face verification does not mathematically prove physical classroom presence. See [docs/research/LIMITATIONS.md](./docs/research/LIMITATIONS.md).

## Documentation Index

See [README.md](./README.md) for links to all architecture, API, security, and deployment documents.
