# Database Dictionary

This document details every table, column, datatype, constraint, and index within the SQLite database.

## Table: `users`
Purpose: Base authentication and identity table.
| Column | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier for the user. |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for Admin/Faculty login). |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hash of the user's password. |
| `role` | VARCHAR(20) | NOT NULL | Role enum: `ADMIN`, `FACULTY`, `STUDENT`. |
| `is_active` | BOOLEAN | DEFAULT 1 | Soft delete / Account deactivation flag. |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation time. |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Last update time. |

*Indexes*: `idx_users_email` (email)

## Table: `students`
Purpose: Extends `users` with student-specific academic information.
| Column | Data Type | Constraints | Purpose |
|---|---|---|---|
| `user_id` | INTEGER | PRIMARY KEY, FOREIGN KEY (`users.id`) | Links to the base user record. |
| `roll_number` | VARCHAR(50) | UNIQUE, NOT NULL | Student's primary login identifier. |
| `first_name` | VARCHAR(100) | NOT NULL | First name. |
| `last_name` | VARCHAR(100) | NOT NULL | Last name. |
| `department_id` | INTEGER | FOREIGN KEY (`departments.id`) | The student's department. |
| `face_profile_active` | BOOLEAN | DEFAULT 0 | Indicates if the student has a valid face embedding. |

*Indexes*: `idx_students_roll_number` (roll_number)

## Table: `biometric_templates`
Purpose: Stores the serialized 128D/512D face embeddings used for 1:1 verification.
| Column | Data Type | Constraints | Purpose |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique record ID. |
| `student_id` | INTEGER | UNIQUE, FOREIGN KEY (`students.user_id`) | The student this template belongs to. |
| `embedding_data` | BLOB | NOT NULL | The binary or JSON representation of the face vector. |
| `version` | INTEGER | DEFAULT 1 | AI Model version used to generate the embedding. |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Enrollment date. |

*Indexes*: `idx_biometrics_student` (student_id)

*(Additional tables follow the same pattern...)*
