# SecureAttend

SecureAttend is a comprehensive, AI-powered attendance tracking system built for educational institutions. It features a robust Python FastAPI backend, a React web administration dashboard, and a Flutter mobile application for students and faculty.

## Project Structure

This repository is organized into two main directories:

- `/backend` - Contains the Python FastAPI server, database models, AI/ML face recognition logic, and the React Admin Dashboard (located in `/backend/admin`).
- `/apk_build` - Contains the Flutter mobile application source code and build configuration for generating the Android APK.

## Features

- **Face Recognition Attendance:** Securely mark attendance using advanced facial recognition and liveness detection.
- **Dynamic QR Codes:** Faculty can generate time-sensitive, dynamic QR codes from the dashboard for students to scan.
- **Real-Time Dashboard:** A responsive React dashboard for administrators and faculty to monitor live attendance sessions, manage users, and generate reports.
- **Cross-Platform Mobile App:** A unified Flutter application with distinct portals for Students (marking attendance, viewing history) and Faculty (managing sessions).

## Tech Stack

- **Backend:** Python, FastAPI, SQLite, SQLAlchemy, InsightFace (AI Models)
- **Frontend (Web):** React, Vite, Tailwind CSS, TypeScript
- **Frontend (Mobile):** Flutter, Dart
- **Security:** Argon2 Password Hashing, JWT Authentication
