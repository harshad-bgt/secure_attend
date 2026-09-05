# Research Gap — SecureAttend AI

## Academic Context

Smart attendance systems combining face recognition, liveness detection, and dynamic QR authentication represent an active research area. This project addresses the gap between theoretical multi-factor attendance protocols and a practical, deployable academic demonstration system.

## Identified Gaps

### G1 — Integrated Multi-Factor LAN Attendance

Most academic implementations focus on single-factor (QR-only or face-only) systems. Few demonstrate integrated face + liveness + dynamic QR on consumer hardware over local networks without cloud dependencies.

**This project addresses:** End-to-end multi-factor pipeline on a single laptop.

### G2 — Admin-Controlled Biometric Enrollment

Self-enrollment introduces consent and quality control issues. This project separates account creation from biometric enrollment with Admin-supervised webcam capture.

### G3 — Dual-Role Mobile Client Architecture

Single APK with backend-authoritative role routing is uncommon in academic projects that typically build separate apps or use manual role selection.

### G4 — Practical SQLite Transaction Design for Concurrent Attendance

Documented patterns for safe concurrent attendance marking with AI inference outside write transactions on SQLite are limited.

## Related Work

| Area | Existing Solutions | Gap |
|------|-------------------|-----|
| Face recognition attendance | OpenCV + LBPH, deepface demos | Limited liveness + QR integration |
| QR attendance | Static QR, Google Forms | No biometric binding |
| Liveness detection | MiniFASNet, FaceX-Zoo | Not integrated with attendance workflow |
| Dynamic QR | TOTP-style tokens | Not combined with face verification |

## Research Questions

1. What is the acceptable false accept/reject rate for ArcFace cosine similarity in classroom lighting conditions?
2. How effective is challenge-response liveness against casual spoofing attempts in academic settings?
3. What QR rotation interval balances usability (scan time) vs security (sharing window)?
4. How does SQLite WAL mode perform with 60 concurrent attendance writes?

These will be evaluated empirically during Phases 4–9.

## Contribution

- Documented architecture for two-agent development (backend + mobile) with stable API contract
- Reproducible local-network deployment model
- Open design documents for face enrollment, verification, liveness, and dynamic QR protocols
- Explicit security limitation documentation (honest threat model)

## Future Research Directions

See [FUTURE_SCOPE.md](./FUTURE_SCOPE.md).
