# SecureAttend AI Error Codes

This document defines the standard machine-readable error codes returned by the backend API. The mobile client and web panel should map these codes to human-readable strings to provide localized and context-aware error messages.

## Error Response Format
All API error responses share a consistent schema:

```json
{
  "error": {
    "code": "category/specific-error",
    "message": "Developer-friendly description of the error."
  }
}
```

## Authentication & Role (HTTP 401 / 403)
| Error Code | HTTP Status | Description |
|---|---|---|
| `auth/invalid-credentials` | 401 | The provided email/roll number and password combination is incorrect. |
| `auth/account-inactive` | 403 | The account has been deactivated by the administrator. |
| `auth/token-expired` | 401 | The access token has expired and must be refreshed. |
| `auth/refresh-invalid` | 401 | The refresh token is invalid or has expired. User must log in again. |
| `auth/unauthorized-role` | 403 | The user is authenticated but does not possess the required role (e.g., Student trying to access Faculty routes). |

## Student Attendance & Liveness (HTTP 400 / 403 / 404 / 409)
| Error Code | HTTP Status | Description |
|---|---|---|
| `attendance/no-face-profile` | 403 | The student does not have an active face profile enrolled by the admin. |
| `attendance/liveness-failed` | 400 | The liveness verification challenge failed (e.g., blink not detected, multiple faces). |
| `attendance/verification-failed` | 403 | The 1:1 face match fell below the similarity threshold. |
| `attendance/face-proof-expired` | 400 | The short-lived face proof token has expired. The student must retake the liveness challenge. |
| `attendance/student-not-enrolled`| 403 | The student is not officially enrolled in the class associated with the scanned QR token. |
| `attendance/duplicate-submission`| 409 | The student has already been marked present for this session. |

## Dynamic QR Validation (HTTP 400 / 404 / 410)
| Error Code | HTTP Status | Description |
|---|---|---|
| `qr/expired` | 410 | The QR token scanned has passed its validity window. |
| `qr/invalid` | 400 | The QR token payload is malformed or signature validation failed. |
| `qr/session-ended` | 410 | The associated attendance session has been explicitly ended by the faculty. |
| `qr/session-not-found` | 404 | The session ID embedded in the QR token does not exist. |

## General / System (HTTP 400 / 404 / 429 / 500)
| Error Code | HTTP Status | Description |
|---|---|---|
| `system/rate-limited` | 429 | Too many requests have been made within a time window. |
| `system/not-found` | 404 | The requested resource (e.g., schedule, profile) does not exist. |
| `system/bad-request` | 400 | The request payload violates schema constraints (e.g., missing required fields). |
| `system/internal-error` | 500 | An unexpected backend exception occurred. |

## Example Error Response
```json
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": {
    "code": "auth/invalid-credentials",
    "message": "The credentials provided do not match our records."
  }
}
```
