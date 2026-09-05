# Camera and Liveness Design

## Overview
The face verification system relies entirely on backend APIs to perform the authoritative 1:1 match and liveness checks. The mobile client's responsibility is solely to capture the requested media at high quality while providing a smooth UX.

## Mobile Dependencies
- `camera`: For accessing the raw camera feed and capturing frames.
- `permission_handler`: To gracefully request and handle denied/restricted camera access.

## Liveness UX Workflow
1. **Fetch Challenge**: App asks the backend `/student/face-verification/challenge` for the required action.
2. **Interpret Response**: The backend responds with specific instructions (e.g., `["look_straight", "blink"]`).
3. **Render Instructions**: The app displays an overlay on the camera feed with localized, human-readable text ("Please look straight at the camera and blink").
4. **Capture Strategy**: 
   - Based on the challenge, the app will capture a short sequence of frames or a high-quality still image.
   - Images are captured using the front-facing camera.
   - Aspect ratio and resolution are optimized for face matching (e.g., avoiding 4K if it causes timeout issues, targeting a backend-specified file size limit).
5. **Upload & Clean**: 
   - Media is temporarily written to the app's cache directory.
   - Uploaded via multipart form data to `/student/face-verification/verify`.
   - **CRITICAL**: The cached files are immediately deleted (`File.delete()`) regardless of whether the upload succeeds or fails.

## Edge Case Handling
- **App Backgrounding**: If the user minimizes the app while the camera is active, the camera controller is disposed to free resources. Upon resume, the liveness state machine reverts to `REQUESTING_LIVENESS_CHALLENGE` to prevent tampered or stale captures.
- **Timeouts**: If the capture takes too long (e.g., user is not acting), the UI cancels the feed and prompts the user to retry.
- **Permissions Denied**: If the user permanently denies camera access, a custom UI instructs them to open OS settings, as the system cannot function without it.
