# Deployment Guide — SecureAttend AI

## Deployment Model

Initial deployment: **single laptop, local network, no cloud infrastructure**.

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend |
| Node.js | 20+ | Admin Portal |
| Git | Latest | Version control |

Phase 4+ additionally requires:
- InsightFace + ONNX Runtime (installed via pip)
- Webcam (for Admin face enrollment)

## Directory Setup (Phase 1+)

```bash
git clone <repository-url>
cd backend
cp .env.example .env
# Edit .env with your secrets and LAN IP
mkdir -p data
```

## Environment Configuration

See [.env.example](../.env.example). Critical settings:

| Variable | Description |
|----------|-------------|
| `HOST=0.0.0.0` | Required for mobile LAN access |
| `PORT=8000` | API port |
| `DATABASE_URL` | SQLite path |
| `JWT_SECRET_KEY` | Change from default |
| `CORS_ORIGINS` | Include Admin Portal origin |

## Starting Services (Phase 1+)

### Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Admin Portal (Development)

```bash
cd apps/admin-web
npm install
npm run dev -- --host 0.0.0.0
```

### Admin Portal (Production Build)

```bash
cd apps/admin-web
npm run build
# Serve dist/ via backend static files or separate server
```

## Database Migrations (Phase 2+)

```bash
cd backend
alembic upgrade head        # Apply migrations
alembic revision --autogenerate -m "description"  # Create new
```

## Seed Data (Phase 2+ / Phase 10)

```bash
python scripts/seed_demo_data.py
```

## Mobile Client Configuration

Flutter APK must point to laptop LAN IP:

```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.105:8000/api/v1
```

See [LOCAL_NETWORK_DEPLOYMENT.md](./architecture/LOCAL_NETWORK_DEPLOYMENT.md).

## Health Verification

```bash
curl http://localhost:8000/api/v1/health
curl http://192.168.1.105:8000/api/v1/health  # From phone browser
```

## Backup and Restore (Phase 10)

### Backup

```bash
# Stop backend first
cp data/secureattend.db data/backups/secureattend_$(date +%Y%m%d).db
```

### Restore

```bash
cp data/backups/secureattend_20260707.db data/secureattend.db
```

## Firewall

See [LOCAL_NETWORK_DEPLOYMENT.md](./architecture/LOCAL_NETWORK_DEPLOYMENT.md) for OS-specific firewall rules.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | Change PORT in .env or kill existing process |
| DB locked | Ensure only one backend instance; check WAL mode |
| AI model download fails | Check internet for first-time model download |
| Mobile can't connect | Verify 0.0.0.0 binding and firewall |

## Production Considerations (Out of Initial Scope)

- TLS/HTTPS with reverse proxy (nginx/caddy)
- PostgreSQL instead of SQLite
- Systemd/Windows Service for auto-start
- Log rotation
- Automated backups

## Phase Status

This guide is a design document in Phase 0. Executable scripts and services are created in Phase 1+.
