# API Integration & Networking Design

## The DIO Client Setup
All network communication flows through a globally configured `Dio` client instance provided via Riverpod (`apiClientProvider`).

### Interceptors
1. **AuthInterceptor**: Automatically injects the `Authorization: Bearer <token>` header into every request requiring authentication.
2. **RefreshTokenInterceptor**: 
   - Intercepts `401 Unauthorized` responses.
   - Pauses all outgoing requests.
   - Makes a single-flight request to `/auth/refresh` using the stored refresh token.
   - If successful, saves new tokens, resumes queued requests, and retries the failed request.
   - If failed, triggers a forced logout and routes the user to the login screen.
3. **LoggingInterceptor**: Logs request/response details in debug mode.

### Network Configuration
- **Base URL**: Loaded dynamically based on the environment (e.g., `--dart-define=API_BASE_URL=http://192.168.1.100:8000/api/v1`).
- **Timeouts**: 
  - Default connection timeout: 10 seconds.
  - Upload timeout (Face verification): 30 seconds to accommodate large media payloads over slower networks.

## Error Mapping Design
The backend will return machine-readable error codes as defined in `docs/api/ERROR_CODES.md` (which is pending). The mobile app will not display raw stack traces or internal server errors to the user.

- **`AppException` Class**: A custom Dart exception class to map HTTP responses into domain errors.
- **Mapping Logic**:
  - `auth/invalid-credentials` -> "The username or password you entered is incorrect."
  - `attendance/liveness-failed` -> "Liveness check failed. Please ensure you are in a well-lit area and follow the instructions."
  - `attendance/qr-expired` -> "This QR code has expired. Please ask the faculty to refresh the code."
  - `network/unreachable` -> "Cannot connect to the server. Please check your network connection."

## Single-Flight Refresh Behavior
To prevent a flood of refresh token requests when multiple API calls fail simultaneously:
- A `Completer<void>? _refreshCompleter` is used inside the `RefreshTokenInterceptor`.
- If `_refreshCompleter` is active, subsequent 401s will `await _refreshCompleter.future` rather than triggering a new refresh API call.

## Safe Retry Policy
- Idempotent requests (GETs, e.g., fetching schedule, profile) may be retried automatically on timeout or network failure.
- Non-idempotent requests (POSTs, e.g., submitting attendance, starting a session, verifying face) **will not be blindly retried** automatically by the client unless specifically dictated by a transaction token from the backend, to prevent duplicate state mutations.
