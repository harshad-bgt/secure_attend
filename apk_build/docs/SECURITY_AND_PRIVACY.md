# Security, Privacy, and Network Configuration

## Storage Security
- **No Local Secrets**: The application source code contains zero hardcoded API keys, JWT secrets, or cryptographic seeds for QR generation. 
- **Token Storage**: `flutter_secure_storage` is used to store `access_token` and `refresh_token`. On Android, this leverages `EncryptedSharedPreferences` backed by the Android Keystore system.
- **Biometric Ephemerality**: Face capture images are written to `getTemporaryDirectory()`. These files are deleted immediately after the API response is received or if the capture flow is cancelled. They are **never** copied to the public gallery or persisted between app sessions.

## Authority and Trust Model
- **Zero Trust Client**: The mobile application does not make any final security decisions. 
  - It does not calculate face embeddings.
  - It does not decide if a user is "real" (liveness).
  - It does not validate QR signatures.
  - It does not override the user's role (Student/Faculty).
- All these responsibilities are delegated to the FastAPI backend.

## Device Privacy Limitations
- Because the app runs on a user's personal device, it operates in an inherently untrusted environment (e.g., rooted devices, screen recording).
- We will attempt to use `flutter_windowmanager` (or similar) to set `FLAG_SECURE` on Android during the Face Verification screen to prevent casual screen recording or screenshots of the liveness challenge. *Note: This does not prevent physical camera recording.*

## Local Network Configuration
Since the primary deployment target is a local network (laptop acting as server, Android phones connecting via Wi-Fi/Hotspot):
1. **Dynamic Base URL**: The API URL cannot be hardcoded as IP addresses will change.
2. **Implementation**: 
   - We will use `--dart-define` for compile-time injection during testing.
   - For physical deployment without recompiling, we will implement a hidden "Developer Options" screen (accessible via rapid taps on the app version number) allowing administrators to manually input the Server IP Address (e.g., `192.168.x.x:8000`).
3. **Cleartext Traffic**: Android blocks HTTP cleartext traffic by default. We must modify `AndroidManifest.xml` to include `android:usesCleartextTraffic="true"` or define a network security configuration specifically allowing the local network subnet, as the local FastAPI server may not have a valid TLS certificate.
