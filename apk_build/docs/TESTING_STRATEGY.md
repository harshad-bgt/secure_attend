# Testing Strategy

## Overview
The mobile client testing strategy aims to validate logic, state management, and UI rendering in isolation before attempting full backend integration testing on physical devices.

## 1. Unit Tests
- **Focus**: Business logic, state machines, data parsing, and interceptor behavior.
- **Targets**:
  - `AuthRepository`: Validating login parsing and error throws.
  - `RoleParser`: Ensuring backend roles correctly map to internal routing enums.
  - `ErrorMapper`: Verifying that backend error strings correctly map to human-readable UI strings.
  - `StudentAttendanceNotifier`: Asserting that state transitions follow the strict requirements (e.g., cannot go from `IDLE` straight to `SCANNING_QR`).
  - `TokenRefreshInterceptor`: Mocking Dio responses to ensure a 401 triggers exactly one refresh request.

## 2. Widget Tests
- **Focus**: UI component rendering and interaction without real network calls.
- **Targets**:
  - **Login Screen**: Validate form validation, loading indicator display, and error text rendering.
  - **Student Shell/Dashboard**: Verify conditional rendering (e.g., "No face profile" warning).
  - **QR Scanner Shell**: Mocking `mobile_scanner` to trigger a simulated barcode detection and verifying the UI moves to the "Submitting" state.
  - **Faculty QR Display**: Mocking a session state to ensure the countdown text decrements and triggers the refresh callback.

## 3. Integration Tests (Mocked)
- **Focus**: Full app flows using `integration_test` on emulators.
- **Methodology**: We will use a Mock Backend (via Mockito or a local mock server) to simulate the FastAPI contract. 
- **Crucial Rule**: Mock integration tests **will not** be presented as proof of real backend integration. They exist solely to prove the Flutter UI navigation and state management work end-to-end.

## 4. Physical Device Verification (Real Backend)
- **Focus**: Hardware interactions (Camera, Network over LAN).
- **Execution**:
  - Requires the Cursor agent to complete the backend APIs.
  - Run debug APK on physical Android devices.
  - Validate Camera permission flows, image capture quality, QR scanning reliability under various lighting conditions.
  - Validate the `usesCleartextTraffic` local network connection works flawlessly.
