# Development Roadmap

This roadmap outlines the strict phase-by-phase execution plan for the SecureAttend AI Mobile App. **No phase will begin until the previous phase is completed and approved.**

## 🟢 Phase 0 — Architecture and API Contract Analysis (Current)
- [x] Inspect repository state.
- [x] Analyze backend API contract (Note: Contract missing, generated requests).
- [x] Document Mobile Architecture, Networking, Auth, and Routing.
- [x] Document State Machines (Student & Faculty).
- [x] Establish Security and Testing strategies.

## 🟡 Phase 1 — Flutter Scaffolding and Core Infrastructure
- Create Flutter project structure.
- Configure dependencies (Riverpod, GoRouter, Dio, Secure Storage).
- Setup Material 3 theme.
- Implement debug diagnostic tools (API Base URL config, network health).

## 🟡 Phase 2 — Authentication and Role Routing
- Implement Login UI.
- Integrate secure token storage and `AuthInterceptor`.
- Implement `RefreshTokenInterceptor` and session restoration.
- Build GoRouter role-based guards.

## 🟡 Phase 3 — Student Dashboard, Schedule, History, Profile
- Build Student shell and bottom navigation.
- Implement data fetching for dashboard, schedule, and history.
- Implement profile view and the "no-face-profile" blocked state.

## 🟡 Phase 4 — Student Camera, Liveness, and Face Verification Flow
- Implement `camera` and `permission_handler`.
- Build the `AttendanceState` machine UI.
- Implement liveness challenge rendering and capture sequence.
- Handle temporary file creation/deletion.

## 🟡 Phase 5 — Student Dynamic QR Scan and Attendance Marking
- Integrate `mobile_scanner`.
- Implement QR parsing (opaque token) and submission logic.
- Handle success/rejection UI and retry loops.

## 🟡 Phase 6 — Faculty Dashboard, Schedule, and Attendance Session Creation
- Build Faculty shell and navigation.
- Implement class schedule fetching.
- Build the UI to select a class and initiate a new attendance session.

## 🟡 Phase 7 — Faculty Dynamic QR Display and Live Attendance
- Implement `qr_flutter` rendering based on backend token.
- Build the countdown timer and auto-refresh logic.
- Implement live short-polling for present/absent student lists.
- Implement session termination.

## 🟡 Phase 8 — Full Backend Integration
- **Dependency**: Requires Cursor agent to have deployed the real FastAPI backend.
- Conduct physical device testing over LAN.
- Validate end-to-end flows for both roles.

## 🟡 Phase 9 — Security, Reliability, and UX Hardening
- Test edge cases (app backgrounding, token expiration, poor network).
- Implement skeleton loaders and empty states.
- Run full unit/widget test suites.

## 🟡 Phase 10 — Final APK and Documentation
- Finalize app icon and metadata.
- Build release APK.
- Complete all deployment documentation.
