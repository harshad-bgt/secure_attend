# System Architecture

## 1. Overall System Architecture
```mermaid
graph TD
    A[React Admin Panel] -->|REST API| C(FastAPI Backend)
    B[Flutter Mobile App] -->|REST API| C
    C --> D[(SQLite Database)]
    C --> E[Face AI Services]
    C --> F[Dynamic QR Service]
    E --> G[Face Detection]
    E --> H[Embedding Generator]
    E --> I[1:1 Verifier]
```

## 2. Authentication Flow
```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB
    
    Client->>API: POST /auth/login (Credentials)
    API->>DB: Query User
    DB-->>API: Return User & Hash
    API->>API: Verify Password
    API-->>Client: Return Access Token & Refresh Token
```

## 3. Face Enrollment Flow (Admin)
```mermaid
sequenceDiagram
    participant AdminWeb
    participant API
    participant AI
    participant DB
    
    AdminWeb->>API: POST /admin/enroll-face (Webcam Image)
    API->>AI: Detect Face & Generate Embedding
    AI-->>API: Vector Data
    API->>DB: Store in BiometricTemplates
    API-->>AdminWeb: 201 Created (Success)
```

## 4. Face Verification Flow (Student)
```mermaid
sequenceDiagram
    participant App
    participant API
    participant AI
    participant DB
    
    App->>API: POST /api/v1/student/face-verification/challenge
    API-->>App: ["blink", "look_straight"]
    App->>App: Capture Liveness Sequence
    App->>API: POST /api/v1/student/face-verification/verify (Images)
    API->>AI: Perform Liveness Check
    API->>DB: Fetch Enrolled Embedding
    API->>AI: Perform 1:1 Match
    AI-->>API: Match Success
    API-->>App: Face Proof Token (Valid for 60s)
```

## 5. Dynamic QR Authentication
```mermaid
sequenceDiagram
    participant FacultyApp
    participant API
    participant StudentApp
    
    FacultyApp->>API: POST /api/v1/faculty/attendance-sessions
    API-->>FacultyApp: QR Token T1
    FacultyApp->>FacultyApp: Render QR T1
    StudentApp->>StudentApp: Scan QR T1
    StudentApp->>API: POST /api/v1/student/attendance/mark/mark (QR T1 + Face Proof)
    API-->>StudentApp: 201 Success
    FacultyApp->>API: GET /api/v1/faculty/attendance-sessions/{session_id}/qr
    API-->>FacultyApp: QR Token T2
```

## 6. Attendance Workflow
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> LivenessChallenge : Start Attendance
    LivenessChallenge --> FaceVerification : Upload Media
    FaceVerification --> ScannerActive : Match Success
    FaceVerification --> LivenessChallenge : Match Failed (Retry)
    ScannerActive --> Submit : Scan QR
    Submit --> Success : Backend Confirms
    Submit --> ScannerActive : Invalid QR (Retry)
    Success --> [*]
```

## 7. Deployment Architecture
```mermaid
graph TD
    subgraph Local LAN
        L[Laptop / Server]
        L --> W[React Static Files]
        L --> F[FastAPI Uvicorn on 0.0.0.0:8000]
        F --> DB[(SQLite file)]
        P1[Faculty Android Device] -.->|Wi-Fi HTTP| F
        P2[Student Android Device] -.->|Wi-Fi HTTP| F
        P3[Student Android Device] -.->|Wi-Fi HTTP| F
    end
```
