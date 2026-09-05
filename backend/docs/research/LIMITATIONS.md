# Limitations — SecureAttend AI

## Security Limitations

### No Physical Presence Proof

The system intentionally does **not** implement:

- GPS location validation
- Geofencing
- Bluetooth beacon proximity
- Wi-Fi SSID/BSSID proximity detection

**Consequence:** Dynamic QR + Face Verification + Liveness does not mathematically prove the student is physically in the classroom. A QR code screenshot could be shared with a remote authenticated student within the token's short lifetime (~15 seconds).

**Mitigations:**
- Very short QR token lifetime (15 seconds)
- Student must be authenticated (login credentials)
- Face verification against enrolled template
- Liveness challenge-response
- Enrollment validation (student must be in class roster)
- Attendance time window
- Duplicate prevention (one mark per session)
- Device metadata hash for audit
- Security event logging

### Basic Liveness Detection

Initial liveness uses challenge-response heuristics (blink, head turn). This is **not production-grade anti-spoofing**.

**Known bypass vectors:**
- Video replay on screen
- Printed photo with cut-out eyes (for blink)
- Pre-recorded video with head movements

**Mitigation path:** Replaceable liveness adapter for stronger models in future.

### Unencrypted HTTP (LAN Demo)

Initial deployment uses HTTP over local network. Tokens and biometric images transit unencrypted on the LAN.

**Mitigation for production:** TLS/HTTPS with local CA or reverse proxy.

## Technical Limitations

### Single Point of Failure

All services run on one laptop. No high availability, load balancing, or failover.

### SQLite Concurrency

SQLite handles moderate concurrent writes but is not ideal for high-throughput multi-server deployments. Sufficient for academic demo (~60 concurrent marks).

### CPU-Only AI Inference

No GPU acceleration assumed. Face verification adds latency (~1-2s per attempt). Multiple simultaneous verifications may queue.

### Network Dependency

Mobile attendance requires continuous connectivity to the laptop backend. No offline mode.

## Privacy Limitations

- Biometric embeddings are stored (required for verification)
- No formal consent management system (operational policy expected)
- No encryption at rest for SQLite database

## Scope Limitations

- No student self-registration
- No student self-enrollment
- Admin-only face enrollment (requires physical Admin + student presence)
- No integration with existing university ERP/SIS
- No email/SMS notification delivery (in-app only initially)

## Academic Project Boundaries

This system is designed for:

- Local network demonstration
- Academic evaluation
- Proof of concept for multi-factor attendance

It is **not** designed for:

- Production deployment at scale
- Regulatory compliance (GDPR biometric provisions, etc.) without additional work
- Adversarial security testing

See [THREAT_MODEL.md](../security/THREAT_MODEL.md) for detailed threat analysis.
