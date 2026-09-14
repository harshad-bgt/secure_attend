# SecureAttend Phase 8 — Geofencing Implementation Plan

> [!CAUTION]
> This is a PLAN ONLY. No implementation has been performed.

## 1. Objective
Implement a Global Campus Geofence requirement for student attendance marking. A student must physically be within the Admin-configured campus radius to successfully submit attendance. This establishes the final piece of the security model: **FACE = WHO, DYNAMIC QR = WHICH SESSION, GEOFENCING = WHERE.**

## 2. Existing Architecture
- The backend `POST /student/attendance/mark` endpoint accepts a QR Token and Face Token, but receives no location data.
- The `AttendanceSession` model lacks location constraints.
- Admin `Settings.tsx` is an empty stub.
- Flutter APK lacks location dependencies and Android GPS permissions.

## 3. Proposed Architecture
A **Global Campus Geofence** model.
The Admin configures the master Campus Latitude, Longitude, and Allowed Radius in the React Admin panel. The Flutter application captures the student's GPS coordinates exactly when scanning the QR code, sending the raw coordinates to the backend. The FastAPI backend calculating the Haversine distance and acting as the final, absolute authority for acceptance or rejection. The client will never compute or transmit a boolean `is_inside_geofence`.

## 4. Database Design
A new singleton model `CampusSettings`:
```python
class CampusSettings(Base):
    __tablename__ = "campus_settings"
    
    id = Column(Integer, primary_key=True, index=True) # Will strictly be 1 for singleton
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Float, nullable=False, default=200.0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```
**Singleton Strategy**: API endpoints modifying this configuration will always `query(CampusSettings).filter(id == 1)` or create it with `id=1` if missing. No multiple records will be supported.

## 5. Migration Plan
- Create an Alembic revision `add_campus_settings`.
- Safe rollout: The migration only adds the new table. It does not alter existing tables or delete data.
- If `CampusSettings` is empty, the `mark_attendance` endpoint should either accept all requests (graceful degradation) or return an explicit HTTP 500/400 (Configuration Missing). The plan opts for **HTTP 400 (Configuration Missing)** to force strict security compliance.

## 6. API Design
**A. Admin Configuration API**
- `GET /api/v1/admin/settings/geofence`: Returns current `CampusSettings` (Admin Only).
- `POST/PUT /api/v1/admin/settings/geofence`: Accepts JSON payload with `latitude`, `longitude`, `radius_meters`. Upserts record `id=1`. Returns `200 OK`. (Admin Only).

**B. Attendance API (`backend/api/schemas.py`)**
- `AttendanceMarkRequest` schema updated to include:
  - `latitude: float`
  - `longitude: float`

## 7. Attendance Flow
1. Faculty starts session (Unchanged).
2. Student scans QR → **Requests Location Permissions & Acquires GPS**.
3. Student passes GPS payload to Face Verification screen.
4. Student verifies Face (Unchanged).
5. Student submits: `{ qr_token, face_proof_token, latitude, longitude }`.
6. Backend validates tokens and session (Unchanged).
7. **Backend calculates Haversine distance against CampusSettings.**
8. If `distance <= radius_meters` → Accept. Else → Reject (HTTP 403 Forbidden).

## 8. Distance Calculation
- **Algorithm**: Haversine Formula (Great-circle distance between two points on a sphere).
- **Validation**: Latitude must be between -90 and +90. Longitude between -180 and +180.
- **Boundary**: `distance <= radius_meters` is ACCEPTED.
- **Admin Validation**: Radius must be strictly > 0. (Recommend a minimum of 50m to avoid GPS drift false-negatives).

## 9. Admin UI
- Enhance `backend/admin/src/pages/Settings.tsx`.
- Form containing: Campus Latitude, Campus Longitude, Allowed Radius (meters).
- Include Save button with loading states, success Toast notifications, and API error handling.
- Ensure restricted access to Admin roles only.

## 10. Flutter Implementation
- **Dependency**: Add `geolocator: ^11.0.0` to `pubspec.yaml`.
- **Flow in `student_qr_scanner.dart`**:
  1. Check `Geolocator.checkPermission()`.
  2. If denied, `Geolocator.requestPermission()`.
  3. If permanently denied or location services disabled, show blocking UI modal.
  4. Fetch location: `Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high)`.
  5. Check `position.isMocked`. If mocked, show warning (though mock-detection on Android is not 100% foolproof, it filters casual tampering).
  6. Pass coordinates to the next routing layer (`student_face_verification.dart`) to eventually build the API payload.

## 11. Android Implementation
- Modify `apk_build/android/app/src/main/AndroidManifest.xml`.
- Add:
  - `<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />`
  - `<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />`
- No background tracking permissions (`ACCESS_BACKGROUND_LOCATION`) will be requested.

## 12. Security Model
- **Fake Coordinates**: Protected. The backend remains the mathematical authority. The client cannot send `is_inside_geofence=True`.
- **Missing Coordinates**: Protected. Pydantic validation on `AttendanceMarkRequest` will block missing fields.
- **Mock GPS**: Mitigated. `geolocator` flags mocked locations via standard Android APIs. Highly sophisticated root-level spoofing is not 100% preventable client-side, but the backend maintains historical logs if needed later.
- **Direct API Bypass**: Protected. Passing fake coordinates manually to the API requires knowing the exact campus coordinates and possessing valid, timed QR/Face tokens.

## 13. Error Handling
- **Flutter**: 
  - "Location permission denied. Cannot mark attendance."
  - "Please enable GPS services."
  - "GPS timeout. Please try again outside."
- **Backend**:
  - `HTTP 403`: "You are outside the campus geofence (Distance: X meters). Attendance denied."
  - `HTTP 422`: "Invalid latitude/longitude format."
  - `HTTP 400`: "Campus geofence configuration is missing. Please contact an Administrator."

## 14. File Impact
1. `backend/api/models.py`: (Add CampusSettings)
2. `backend/api/schemas.py`: (Update AttendanceMarkRequest, create GeofenceSettings schema)
3. `backend/api/routes/admin.py`: (Create GET/POST endpoints for Geofence config)
4. `backend/api/routes/student_attendance.py`: (Add Haversine math and geofence rejection in `mark_attendance`)
5. `backend/admin/src/pages/Settings.tsx`: (Build Admin UI)
6. `apk_build/pubspec.yaml`: (Add geolocator)
7. `apk_build/android/app/src/main/AndroidManifest.xml`: (Add location permissions)
8. `apk_build/lib/screens/student_qr_scanner.dart`: (Capture GPS and pass to Face screen)
9. `apk_build/lib/screens/student_face_verification.dart`: (Submit GPS with final payload)

## 15. Testing Plan
- **Database**: Run alembic migration, verify singleton restriction.
- **Backend API**: Send valid/invalid coordinates directly to `/mark`. Validate Haversine math.
- **Flutter UI**: Deny permissions and ensure fallback UI correctly blocks progression.
- **End-to-End**: Admin configures campus → Faculty starts session → Student inside campus scans QR/Face → Success. Student walks outside campus → Rejected.
- **Integrity Baseline**: Restore DB to 360 Students, 20 Faculty, 0 Sessions, 0 Attendance post-testing.

## 16. Migration Safety
The Alembic migration strictly creates a new isolated table (`campus_settings`). It does not modify, drop, or alter existing tables (`users`, `attendance_sessions`, etc.). Rollback is a simple `drop_table`. 

## 17. Performance Considerations
- Database: Fetching the singleton `CampusSettings` is an O(1) indexed primary key lookup (`id=1`).
- Math: Python's `math` module calculating Haversine is effectively instant (O(1)). No heavy PostGIS queries are executed.

## 18. Implementation Order
1. Database Model (`models.py`)
2. Alembic Migration
3. Backend Schemas (`schemas.py`)
4. Admin Backend Routes (`admin.py`)
5. Haversine Math & Validation in Attendance Route (`student_attendance.py`)
6. React Admin UI (`Settings.tsx`)
7. Android Permissions (`AndroidManifest.xml`)
8. Flutter Dependency (`pubspec.yaml`)
9. Flutter UX and API submission (`student_qr_scanner.dart`, etc.)
10. Complete Manual Testing.

## 19. Rollback Considerations
If Geofencing causes catastrophic friction on launch day, it can be instantly disabled by modifying `student_attendance.py` to bypass the distance check (1 line change), or by setting the `radius_meters` to `9999999` via the Admin Panel. 

## 20. Protected Existing Functionality
The following systems MUST REMAIN UNTOUCHED AND FUNCTIONAL:
- Phase 5 RBAC and FacultySubjectAssignment authorization.
- Phase 7 Faculty concurrency lock (1 active session maximum).
- Dynamic QR generation and expiry workflows.
- Face enrollment and verification matching logic.
- Student JWT authentication flow.
