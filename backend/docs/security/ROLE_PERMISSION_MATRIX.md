# Role and Permission Matrix — SecureAttend AI

## Roles

| Role | Portal/App | Description |
|------|-----------|-------------|
| ADMIN | Admin Web Portal | Full system administration |
| FACULTY | Flutter APK | Attendance session management |
| STUDENT | Flutter APK | Attendance marking, schedule viewing |

Users have exactly one role. Role is assigned at account creation and returned authoritatively at login.

## Permission Model

Permissions are checked on the backend for every protected endpoint. Frontend route guards are UX-only.

### Permission Codes

| Code | Description |
|------|-------------|
| `admin:dashboard:view` | View admin dashboard |
| `admin:students:manage` | CRUD students |
| `admin:faculty:manage` | CRUD faculty |
| `admin:academic:manage` | Manage academic entities |
| `admin:attendance:view` | View attendance records |
| `admin:attendance:correct` | Manual attendance corrections |
| `admin:face-enrollment:manage` | Face enrollment operations |
| `admin:reports:view` | View and export reports |
| `admin:settings:manage` | System settings |
| `admin:audit:view` | View audit logs |
| `faculty:sessions:create` | Start attendance sessions |
| `faculty:sessions:manage` | Manage own active sessions |
| `faculty:sessions:view` | View session details and history |
| `faculty:schedule:view` | View faculty schedule |
| `student:attendance:mark` | Mark attendance |
| `student:face-verification:perform` | Face verification flow |
| `student:schedule:view` | View student schedule |
| `student:profile:view` | View own profile |
| `student:notifications:view` | View notifications |

## Role-Permission Mapping

| Permission | ADMIN | FACULTY | STUDENT |
|-----------|:-----:|:-------:|:-------:|
| admin:dashboard:view | ✓ | | |
| admin:students:manage | ✓ | | |
| admin:faculty:manage | ✓ | | |
| admin:academic:manage | ✓ | | |
| admin:attendance:view | ✓ | | |
| admin:attendance:correct | ✓ | | |
| admin:face-enrollment:manage | ✓ | | |
| admin:reports:view | ✓ | | |
| admin:settings:manage | ✓ | | |
| admin:audit:view | ✓ | | |
| faculty:sessions:create | | ✓ | |
| faculty:sessions:manage | | ✓ | |
| faculty:sessions:view | | ✓ | |
| faculty:schedule:view | | ✓ | |
| student:attendance:mark | | | ✓ |
| student:face-verification:perform | | | ✓ |
| student:schedule:view | | | ✓ |
| student:profile:view | | ✓ | ✓ |
| student:notifications:view | | | ✓ |

Note: FACULTY has `student:profile:view` for own profile via `/mobile/me`.

## Endpoint Authorization Matrix

| Endpoint | ADMIN | FACULTY | STUDENT |
|----------|:-----:|:-------:|:-------:|
| POST /auth/login | ✓ | ✓ | ✓ |
| POST /auth/refresh | ✓ | ✓ | ✓ |
| POST /auth/logout | ✓ | ✓ | ✓ |
| GET /mobile/me | ✓ | ✓ | ✓ |
| GET /admin/* | ✓ | | |
| GET /student/* | | | ✓ |
| POST /api/v1/student/attendance/mark/mark/mark | | | ✓ |
| GET /faculty/* | | ✓ | |

## Authorization Rules

1. JWT `sub` claim identifies the user — never accept client-provided user ID
2. Role extracted from JWT claims, validated against DB on sensitive operations
3. Faculty can only manage sessions they created (or are assigned to)
4. Students can only access their own profile, history, and verification
5. Admin operations require ADMIN role — no elevation path from mobile

## Implementation (Phase 2+)

```python
# Dependency pattern
async def require_role(*roles: RoleName):
    def checker(user: User = Depends(get_current_user)):
        if user.role.name not in roles:
            raise ForbiddenError("auth/insufficient-permissions")
        return user
    return checker
```
