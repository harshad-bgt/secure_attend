# Faculty Session State Machine

## Overview
The Faculty attendance session workflow dictates how a faculty member initiates, monitors, and terminates a class attendance window. The backend is the sole authority for generating the QR codes and maintaining the official "present" list.

## State Definitions
The `FacultySessionState` manages the lifecycle of the active session:

1. **IDLE**: The faculty is viewing their schedule and has not selected a class.
2. **CREATING_SESSION**: The faculty has selected a class and clicked "Start Attendance". A network request is sent to the backend.
3. **SESSION_ACTIVE**: The backend has created the session. The mobile app receives the first QR token, expiration time, and session ID.
4. **REFRESHING_QR**: The current QR token has expired (or is about to expire based on the backend's countdown). The app requests a new token.
5. **POLLING_ATTENDANCE**: (Concurrent with SESSION_ACTIVE). The app periodically requests the updated present/absent list from the backend.
6. **ENDING_SESSION**: The faculty pressed "End Session". A confirmation dialog was accepted, and the termination request is sent.
7. **SESSION_ENDED**: The backend successfully closed the session. Navigate to the session summary screen.
8. **ERROR**: Network or backend error occurred during creation, refreshing, or ending.

## Dynamic QR Display Logic
- **Server Authority**: The app does **NOT** generate QR tokens or use a secret key locally to sign them. 
- **Render Loop**: 
  1. Fetch opaque token string from backend.
  2. Read `expires_at` timestamp from the response.
  3. Calculate local duration remaining (compensating for network latency if applicable, though relying strictly on the server's window is preferred).
  4. Display token as a QR code using `qr_flutter`.
  5. Display visual countdown.
  6. Trigger `/faculty/attendance-sessions/{session_id}/qr` a few seconds before expiration to ensure seamless scanning.

## Live Polling
- If WebSocket support is not provided in the final backend contract, the app will use standard HTTP short-polling (e.g., every 5 seconds) to fetch the updated attendee list.
- **Resource Management**: Polling must instantly halt if the app is put in the background, the session ends, or the user navigates away.
