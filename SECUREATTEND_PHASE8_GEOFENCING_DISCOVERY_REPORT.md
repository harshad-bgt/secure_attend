# SecureAttend Phase 8 — Geofencing Discovery Report

## 1. Existing Location Infrastructure
- **Current State**: None.
- After a comprehensive search of the entire project repository (Backend, DB Models, Admin React, Flutter APK), there is absolutely **no existing location, GPS, latitude, longitude, or geofence infrastructure**.

## 2. Database Findings
- Existing models (`models.py`) do **not** contain campus coordinates, attendance location, or allowed radius.
- The `AttendanceSession` model currently stores `faculty_id`, `subject_id`, `division_id`, timestamps, and QR data, but no spatial data.

## 3. Backend Findings
- The `POST /student/attendance/mark` endpoint in `backend/api/routes/student_attendance.py` strictly validates the Face Proof Token, QR Token, Session Liveness, and Duplicate checking.
- It accepts an `AttendanceMarkRequest` schema that currently does not request or parse GPS coordinates.

## 4. Attendance-Flow Findings
The current flow is:
1. Faculty starts session → QR generated.
2. Student scans QR → verifies face → Face Token generated.
3. Student submits Face Token + QR Token to `mark_attendance`.
**Integration Point**: Geofence validation MUST occur at Step 3 (`mark_attendance`). The backend must calculate the distance between the student's payload coordinates and the trusted campus coordinates before committing the `AttendanceRecord`.

## 5. Admin Findings
- The Admin Panel has a generic `Settings.tsx` stub page. This is the optimal location for a global "Campus Geofence Configuration" (Latitude, Longitude, Radius in meters).

## 6. Faculty Findings
- Faculty currently just click "Start Attendance".
- **Design Choice**: Unless we want per-classroom dynamic geofences (which adds heavy UX friction for faculty having to stand in the center of the room to grab coordinates), a global campus geofence is vastly superior for UX.

## 7. Flutter Findings
- Flutter uses `student_qr_scanner.dart` to submit the final attendance payload.
- Flutter will need a new dependency (e.g., `geolocator`) to fetch GPS coordinates before triggering the `/mark` API call.

## 8. Android Findings
- `AndroidManifest.xml` lacks `ACCESS_FINE_LOCATION` and `ACCESS_COARSE_LOCATION` permissions. These will need to be added.

## 9. Security Risks
- **Spoofing**: A student can use GPS spoofing apps ("Mock Locations").
- **Mitigation**: The Flutter `geolocator` package can detect if a location is mocked (`isMocked`). The backend must remain the ultimate authority and should ideally log coordinate history to detect teleportation anomalies.
- **Backend Authority**: The Flutter app must ONLY send `latitude` and `longitude`. The backend must independently calculate the Haversine distance and enforce the radius. Never allow the client to send a boolean `is_inside_geofence`.

## 10. Recommended Architecture
**Global Campus Geofence**
- **A.** Add a singleton `CampusSettings` model to the DB containing `center_latitude`, `center_longitude`, and `radius_meters`.
- **B.** Admin configures this once via `Settings.tsx`.
- **C.** Flutter `geolocator` fetches GPS (rejecting mock locations) during the QR scan phase.
- **D.** Flutter sends `lat/lon` in `AttendanceMarkRequest`.
- **E.** FastAPI `mark_attendance` fetches `CampusSettings`, calculates Haversine distance, and rejects if `distance > radius_meters`.

## 11. Proposed Data-Model Changes
- **New Model**: `CampusSettings` (id, latitude, longitude, radius).
- Alternatively, add `latitude` and `longitude` to the existing `AttendanceSession` if dynamic per-classroom geofencing is preferred over a global campus geofence. (Global is recommended for MVP).

## 12. Proposed API Changes
- **Update**: `AttendanceMarkRequest` schema gets `latitude: float`, `longitude: float`.
- **New**: `GET/POST /admin/settings/geofence` to manage the trusted coordinates.

## 13. Proposed UI Changes
- **Admin Panel**: Update `Settings.tsx` with a simple form to set Campus Latitude, Longitude, and Allowed Radius (e.g., 500 meters).

## 14. Proposed Flutter Changes
- Add `geolocator` to `pubspec.yaml`.
- Request Android location permissions dynamically.
- Modify `student_qr_scanner.dart` to await GPS lock before API submission.

## 15. File-by-file Impact Analysis
- `backend/api/models.py`: Required (Add CampusSettings or modify AttendanceSession).
- `backend/api/schemas.py`: Required (Update AttendanceMarkRequest).
- `backend/api/routes/student_attendance.py`: Required (Add Haversine math and rejection logic).
- `backend/admin/src/pages/Settings.tsx`: Required (Add UI form).
- `apk_build/pubspec.yaml`: Required (Add geolocator).
- `apk_build/android/app/src/main/AndroidManifest.xml`: Required (Add GPS permissions).
- `apk_build/lib/screens/student_qr_scanner.dart`: Required (Fetch GPS and append to payload).

## 16. Testing Strategy
- **Unit**: Python Haversine math logic.
- **Integration**: API rejecting invalid coordinates vs accepting valid ones.
- **E2E**: Flutter app requesting permission, getting GPS, and hitting API.

## 17. Risks and Limitations
- **Indoor GPS Accuracy**: Classrooms deep inside concrete buildings often fail to get a GPS lock. The radius must be generous (e.g., 200-500 meters) to account for GPS drift and indoor dead zones.
- **Battery Impact**: Fetching high-accuracy GPS consumes battery. Fetch should only be triggered precisely when scanning the QR code, not running in the background.

## 18. Items that must NOT be changed
- Existing RBAC authorization.
- The Face Verification workflow.
- The Dynamic QR expiry workflow.
- Phase 7 Faculty concurrency logic.
