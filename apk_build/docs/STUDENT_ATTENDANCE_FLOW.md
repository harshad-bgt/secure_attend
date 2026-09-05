# Student Attendance Workflow State Machine

## Overview
The student attendance process is highly sensitive and multi-stepped. To prevent users from skipping required verification phases or getting stuck in inconsistent UI states, the workflow is strictly enforced using a finite state machine implemented via Riverpod (`StateNotifier` / `Notifier`).

## State Definitions
The `AttendanceState` enum defines the exact step the user is in:

1. `IDLE`: Initial state. User has pressed "Mark Attendance".
2. `CHECKING_REQUIREMENTS`: Validating if the backend indicates the student has an enrolled face profile. If none exists, transition to `ERROR` with a specific code.
3. `REQUESTING_CAMERA_PERMISSION`: Checking and requesting platform camera access.
4. `REQUESTING_LIVENESS_CHALLENGE`: Fetching the specific liveness sequence (e.g., "blink", "turn right") from the backend.
5. `PERFORMING_LIVENESS`: Displaying instructions and streaming the camera feed for the user to perform the challenge.
6. `CAPTURING_FACE`: Taking the required frames based on the backend challenge.
7. `UPLOADING_VERIFICATION_MEDIA`: Sending the encrypted/compressed media to the backend.
8. `VERIFYING_FACE`: Waiting for the backend's 1:1 match and liveness decision.
9. `FACE_VERIFIED`: Backend successfully verified the face and returned a short-lived token/proof.
10. `OPENING_QR_SCANNER`: Activating the mobile scanner hardware.
11. `SCANNING_QR`: Waiting for a valid QR payload.
12. `SUBMITTING_ATTENDANCE`: Sending the QR token + Face verification proof to the backend.
13. `ATTENDANCE_SUCCESS`: Backend confirmed attendance. Display receipt.
14. `ATTENDANCE_REJECTED`: Backend rejected the attendance (expired QR, outside geo-fence, session ended).
15. `ERROR`: Generic/Network error state allowing retry of the safe steps.

## Transitions & Guardrails
- **No Skipping**: A user cannot transition to `OPENING_QR_SCANNER` unless the state is currently `FACE_VERIFIED` and the backend proof token is held in memory.
- **Expiration Handling**: If the QR scan takes too long, the face proof may expire (dictated by the backend). In this case, the state reverts to `REQUESTING_LIVENESS_CHALLENGE`.
- **Cancellation**: If the user presses "Back" at any point before `SUBMITTING_ATTENDANCE`, the state reverts to `IDLE` and all temporary media/tokens are securely wiped.

## Security Rule
The client **does not** mark attendance locally. The success UI is purely a reflection of a HTTP 200/201 response from the attendance submission endpoint.
