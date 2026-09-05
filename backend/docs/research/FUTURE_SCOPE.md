# Future Scope — SecureAttend AI

## Near-Term (Post Phase 10)

| Feature | Description | Phase |
|---------|-------------|-------|
| TLS/HTTPS | Local CA or mkcert for encrypted LAN | 10+ |
| Stronger liveness | MiniFASNet or MediaPipe temporal analysis | 10+ |
| buffalo_l upgrade | Better accuracy on capable hardware | 4+ |
| WebSocket live updates | Replace faculty polling with WS push | 8+ |
| Email notifications | SMTP integration for alerts | 8+ |

## Medium-Term

| Feature | Description |
|---------|-------------|
| PostgreSQL migration | Multi-server deployment |
| Redis caching | Session and token caching |
| Geofencing (optional) | Wi-Fi BSSID or GPS as supplementary signal |
| BLE beacon proximity | Optional classroom presence hint |
| Multi-campus support | Department hierarchy expansion |
| Parent/guardian portal | Attendance visibility for guardians |
| ERP integration | Import students from university SIS |

## Long-Term

| Feature | Description |
|---------|-------------|
| Edge AI on mobile | On-device face detection, server verification |
| Federated learning | Privacy-preserving model improvement |
| Hardware security module | TPM-backed device attestation |
| Cloud deployment | Azure/AWS with auto-scaling |
| iOS support | Cross-platform Flutter |
| Anti-spoof ML model | Production-grade passive liveness |

## AI Model Roadmap

1. **Phase 4:** InsightFace buffalo_sc (current selection)
2. **Phase 9:** Benchmark buffalo_l, evaluate threshold
3. **Future:** MiniFASNet for passive liveness, ArcFace R100 for accuracy

## Infrastructure Roadmap

1. **Phase 1–10:** Single laptop, SQLite, HTTP
2. **Future:** Docker Compose with PostgreSQL + Redis
3. **Future:** Kubernetes for institutional deployment

## Not Planned

- Training face recognition models from scratch
- Blockchain-based attendance (unnecessary complexity)
- Separate Student/Faculty APKs
- Student self-enrollment
