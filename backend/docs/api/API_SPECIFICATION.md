# SecureAttend AI - REST API Specification

This document provides a human-readable specification of the SecureAttend API. It is strictly synchronized with `openapi.json`.

## Base URL
`/api/v1`

## Common Headers
- `Authorization`: `Bearer <jwt_access_token>` (Required for all endpoints except `/auth/login` and `/auth/refresh`)
- `Content-Type`: `application/json` (unless using multipart/form-data for face uploads)

---

## 1. System Endpoints

### Health Check
`GET /api/v1/health`

**Description:** Checks if the backend system is online.

**Response:**
```json
{
  "status": "ok",
  "environment": "development"
}
```

## Authentication

### User Login
`POST /auth/login`
- **Required Role**: None
- **Authentication**: None
- **Validation Rules**: `identifier` must be valid email or roll number, `password` min 8 chars.
- **Request**:
```json
{
  "identifier": "S12345678",
  "password": "studentpassword"
}
```
- **Response** (200 OK):
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG...",
  "role": "STUDENT",
  "profile": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@secureattend.com"
  }
}
```
- **Possible Error Codes**: `auth/invalid-credentials`, `auth/account-inactive`
- **Example Error Response** (401 Unauthorized):
```json
{
  "error": {
    "code": "auth/invalid-credentials",
    "message": "The credentials provided do not match our records."
  }
}
```

### 1.2 Refresh Token
`POST /auth/refresh`
- **Required Role**: None
- **Authentication**: None (Uses refresh token payload)
- **Request**:
```json
{
  "refresh_token": "eyJhbG..."
}
```
- **Response** (200 OK):
```json
{
  "access_token": "eyJhbG...",
  "refresh_token": "eyJhbG..."
}
```
- **Possible Error Codes**: `auth/refresh-invalid`

### 1.3 Logout
`POST /auth/logout`
- **Required Role**: Any
- **Authentication**: Bearer Token
- **Request**: Empty body
- **Response** (200 OK): `{"message": "Logged out successfully"}`
- **Possible Error Codes**: `auth/token-expired`

### 1.4 Get Current User (Me)
`GET /api/v1/mobile/me`
- **Required Role**: Any
- **Authentication**: Bearer Token
- **Request**: N/A
- **Response** (200 OK): Profile data based on role.

---

## 2. Student Endpoints

### 2.1 Get Today's Schedule
`GET /student/schedule/today`
- **Required Role**: `STUDENT`
- **Authentication**: Bearer Token
- **Response** (200 OK):
```json
[
  {
    "schedule_id": 101,
    "subject_name": "Data Structures",
    "faculty_name": "Dr. Smith",
    "start_time": "10:00:00",
    "end_time": "11:00:00"
  }
]
```

### 2.2 Request Liveness Challenge
`POST /api/v1/student/face-verification/challenge`
- **Required Role**: `STUDENT`
- **Authentication**: Bearer Token
- **Response** (200 OK):
```json
{
  "challenges": ["look_straight", "blink"]
}
```

### 2.3 Verify Face
`POST /api/v1/student/face-verification/verify`
- **Required Role**: `STUDENT`
- **Authentication**: Bearer Token
- **Content-Type**: `multipart/form-data`
- **Request**: File upload `image` (JPEG/PNG)
- **Validation Rules**: Max 5MB file size. Valid image format.
- **Response** (200 OK):
```json
{
  "face_proof_token": "proof123",
  "expires_in_seconds": 60
}
```
- **Possible Error Codes**: `attendance/no-face-profile`, `attendance/liveness-failed`, `attendance/verification-failed`

### 2.4 Submit Attendance (QR + Face)
`POST /api/v1/student/attendance/mark/mark`
- **Required Role**: `STUDENT`
- **Authentication**: Bearer Token
- **Request**:
```json
{
  "qr_token": "eyJhbG...",
  "face_proof_token": "proof123"
}
```
- **Response** (201 Created):
```json
{
  "message": "Attendance marked successfully.",
  "subject_name": "Data Structures",
  "timestamp": "2026-07-07T10:15:00Z"
}
```
- **Possible Error Codes**: `attendance/duplicate-submission`, `attendance/face-proof-expired`, `qr/expired`, `qr/invalid`, `qr/session-not-found`

---

## 3. Faculty Endpoints

### 3.1 Start Attendance Session
`POST /api/v1/faculty/attendance-sessions`
- **Required Role**: `FACULTY`
- **Authentication**: Bearer Token
- **Validation Rules**: `schedule_id` must belong to the logged-in faculty.
- **Request**:
```json
{
  "schedule_id": 101
}
```
- **Response** (201 Created):
```json
{
  "session_id": "sess_001",
  "current_qr": "eyJhbG...",
  "expires_at": "2026-07-07T10:05:00Z"
}
```
- **Possible Error Codes**: `system/bad-request`

### 3.2 Refresh QR Code
`GET /api/v1/faculty/attendance-sessions/{session_id}/qr`
- **Required Role**: `FACULTY`
- **Authentication**: Bearer Token
- **Request**: Empty Body
- **Response** (200 OK):
```json
{
  "current_qr": "eyJhbG...",
  "expires_at": "2026-07-07T10:05:15Z"
}
```
- **Possible Error Codes**: `qr/session-ended`

### 3.3 Live Attendance
`GET /api/v1/faculty/attendance-sessions/{session_id}/live`
- **Required Role**: `FACULTY`
- **Authentication**: Bearer Token
- **Response** (200 OK):
```json
{
  "present_count": 45,
  "total_enrolled": 60,
  "present_students": [
    {"roll_no": "S123", "name": "John Doe", "timestamp": "2026-07-07T10:02:00Z"}
  ]
}
```

### 3.4 End Session
`POST /api/v1/faculty/attendance-sessions/{session_id}/end`
- **Required Role**: `FACULTY`
- **Authentication**: Bearer Token
- **Request**: Empty Body
- **Response** (200 OK): `{"message": "Session ended successfully."}`
