# QR Scanner and Display Design

## Faculty: Dynamic QR Display
The Faculty device acts as the attendance beacon by displaying a backend-generated, time-limited Dynamic QR token.

- **Dependency**: `qr_flutter` (for rendering QR codes).
- **Security Rule**: The mobile app must **never** contain the cryptographic secret used to sign or generate these tokens. The app strictly fetches the token payload (`"string"`) via the `/faculty/attendance-sessions/{session_id}` endpoint and renders it.
- **Refresh Mechanism**: The backend specifies an `expires_at` timestamp. A `Timer` is initialized to trigger a token refresh API call 3-5 seconds before expiration. If the network drops, the QR is replaced with a "Loading/Offline" state to prevent students from scanning an expired token.
- **Presentation**: Displayed prominently in the center of the active session screen, with a visual progress bar or countdown text showing remaining seconds until the next refresh.

## Student: QR Scanner
The Student device scans the Faculty's QR code to submit their attendance.

- **Dependency**: `mobile_scanner` (hardware-accelerated barcode scanning).
- **Activation Rule**: The scanner UI is completely inaccessible until the student has successfully completed the face verification and liveness challenge.
- **Scanning Logic**:
  1. Once active, the scanner streams frames to the barcode detector.
  2. Upon detecting a QR code, the scanner is immediately **paused** to prevent a flood of duplicate reads.
  3. The raw string payload is treated as an opaque token (the client does NOT attempt to decode or validate its cryptographic signature).
  4. The client packages the QR token with the short-lived face verification proof (obtained from the previous step) and sends a POST request to `/student/attendance/mark`.
- **Handling Outcomes**:
  - **Success**: Display receipt, close scanner.
  - **Error (Duplicate)**: Inform user they are already marked present.
  - **Error (Expired QR)**: Inform user to wait for the faculty's QR to refresh, then resume the scanner.
  - **Error (Expired Face Proof)**: Inform user they took too long to scan. Route back to liveness capture.
  - **Error (Network)**: Provide a "Retry Submit" button for the same QR token payload.
