# SecureAttend AI Mobile Architecture

## Core Design Principles
1. **Feature-First Clean Architecture**: Codebase is structured by feature rather than layer to improve modularity and maintainability.
2. **Single APK, Multiple Roles**: A single unified APK is delivered. The backend dictates the authenticated user's role (Student/Faculty). Role logic is strictly enforced via routing guards and UI conditional rendering, never assuming local state overrides backend authority.
3. **Reactive State Management**: Utilizing **Riverpod** for robust dependency injection, predictable state mutations, and reactivity without excessive boilerplate.
4. **Declarative Navigation**: Utilizing **GoRouter** to maintain router state as a function of the application state (e.g. auth and role status).
5. **No Local Authority**: The mobile app does NOT perform authoritative face verification, liveness checks, or generate QR signing secrets. The backend is the sole authority.

## Directory Structure
```text
lib/
├── app/
│   ├── app.dart              # Root widget
│   └── bootstrap.dart        # Initialization (Logger, Crashlytics, Error handling)
├── core/
│   ├── config/               # Environment config (API base URLs, timeouts)
│   ├── constants/            # Hardcoded values, dimensions, assets
│   ├── errors/               # Centralized error mapping from backend codes
│   ├── network/              # Dio client, Interceptors, Connectivity checks
│   ├── routing/              # GoRouter configuration & guards
│   ├── security/             # Secure storage abstraction (Tokens, temporary biometrics)
│   ├── theme/                # Material 3 theme (Light/Dark)
│   └── utils/                # General helpers, extensions, logging
├── features/
│   ├── auth/                 # Login, Token refresh, Logout, Session restore
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   ├── student/
│   │   ├── dashboard/
│   │   ├── schedule/
│   │   ├── attendance/       # Liveness UI, Capture, QR Scan, Submission
│   │   ├── history/
│   │   └── profile/
│   └── faculty/
│       ├── dashboard/
│       ├── schedule/
│       ├── sessions/         # Start/End session, QR render, Countdown, Live count
│       └── history/
├── shared/
│   ├── models/               # Common data classes (User Profile, API Responses)
│   ├── providers/            # Global state (App-wide loading, connectivity)
│   └── widgets/              # Reusable UI components (Buttons, Loaders, Dialogs)
└── main.dart                 # Entry point
```

## State Management Approach
- **Providers (Riverpod)**:
  - `authProvider`: Manages session state (Authenticated vs Unauthenticated) and user role.
  - `apiClientProvider`: Provides the configured Dio instance.
  - Feature-specific providers (e.g., `attendanceStateProvider`, `facultySessionProvider`) are scoped to their respective features.
- **StateNotifier / Notifier**: Complex business logic like the Student Attendance State Machine will be encapsulated in Riverpod Notifiers to ensure UI cleanly reflects the underlying state (IDLE -> CHECKING_REQUIREMENTS -> CAPTURING_FACE, etc.).

## App Initialization Flow
1. Load environment variables.
2. Initialize core services (FlutterSecureStorage, SharedPreferences).
3. Check for existing session token (`authProvider.init()`).
4. If a token exists, decode role and navigate to the respective dashboard.
5. If no token, or token is invalid, navigate to Login.
