# Routing and Authentication Design

## Role-Aware Routing with GoRouter
The application uses **GoRouter** to declaratively enforce role-based access control directly derived from the backend's provided profile token.

### Router State
The router depends on an `AuthState` object exposed by Riverpod (`authProvider`):
```dart
enum AuthStatus { unknown, unauthenticated, authenticatedStudent, authenticatedFaculty }
```

### Route Guards (Redirects)
A global `redirect` function inside the GoRouter configuration ensures that users can only access routes appropriate for their state:

1. **Unauthenticated**: All attempts to access `/student/*` or `/faculty/*` are redirected to `/login`.
2. **Authenticated Student**: All attempts to access `/faculty/*` or `/login` are redirected to `/student/dashboard`.
3. **Authenticated Faculty**: All attempts to access `/student/*` or `/login` are redirected to `/faculty/dashboard`.
4. **Unknown**: Displays a Splash/Loading screen while the stored token is retrieved and validated.

### Navigation Tree
- `/` (Splash Screen)
- `/login` (Login Screen)
- `/student` (Student Shell Route - Bottom Navigation Bar)
  - `/student/dashboard`
  - `/student/schedule`
  - `/student/history`
  - `/student/profile`
  - `/student/attendance/mark` (Full-screen flow, hidden from bottom nav)
- `/faculty` (Faculty Shell Route - Bottom Navigation Bar)
  - `/faculty/dashboard`
  - `/faculty/schedule`
  - `/faculty/history`
  - `/faculty/profile`
  - `/faculty/attendance-sessions/{session_id}` (Full-screen flow, QR display)

## Token Lifecycle and Security

1. **Secure Storage**: Access tokens and Refresh tokens are stored exclusively using `flutter_secure_storage` (encrypted Keystore/Keychain). They are **never** logged to the console.
2. **Session Restoration**: On app startup, `bootstrap.dart` reads the secure storage. If tokens exist, it briefly queries a `/mobile/me` endpoint (or decodes the JWT if applicable and safe) to determine the role and validate expiration.
3. **Token Expiration**: Handled reactively by the `RefreshTokenInterceptor`.
4. **Logout Flow**: 
   - User explicitly logs out OR Refresh token expires.
   - Clears all tokens from `flutter_secure_storage`.
   - Clears all cached profile/attendance data.
   - Deletes any temporary files (biometrics, cache).
   - Sets `authProvider` to `unauthenticated`.
   - GoRouter automatically redirects to `/login`.
