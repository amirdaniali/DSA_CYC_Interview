"""
update_readme.py

This script generates/updates README.md with a full explanation of the project:
- Setup guide
- Custom user model
- Serializers
- API endpoints
- Tests
- Documentation generation
"""

README_CONTENT = """# Django Queue API Backend

## Overview
This project is a Django REST Framework backend for managing coding practice sessions and signups.
It provides JWT authentication, custom user accounts, strict permissions, automated tests, and
self-documenting API docs via OpenAPI/Swagger.

---

## Features

### 1. Custom User Model
- Defined in `accounts.models.CustomUser`.
- Extends Django's `AbstractUser` with fields like `discord_username`.
- Integrated with Django admin for management.

### 2. Models
- **Session**: Represents a coding practice session with date, time, capacity, and active status.
- **Signup**: Represents a user's signup for a session, linked to `CustomUser`.

### 3. Serializers
- **SessionSerializer**: Validates and serializes session data.
- **SignupSerializer**: Validates signups, automatically attaches the authenticated user, and enforces strict field validation.

### 4. Permissions
- Sessions can only be created/updated/deleted by admins.
- Signups can only be updated/deleted by their owner or an admin.
- Public endpoints allow listing sessions and signups.

### 5. Authentication
- JWT authentication via `rest_framework_simplejwt`.
- Endpoints:
  - `POST /api/token/` → obtain access + refresh tokens.
  - `POST /api/token/refresh/` → refresh access token.

### 6. API Documentation
- Powered by **drf-spectacular**.
- Endpoints:
  - `/api/schema/` → machine-readable OpenAPI JSON.
  - `/api/docs/swagger/` → interactive Swagger UI.
  - `/api/docs/redoc/` → clean Redoc documentation.
- Docs auto-generate from serializers and viewsets, with optional `extend_schema` decorators for clarity.

### 7. Tests
- Located in `homepage/tests/test_api.py`.
- Cover all behaviors:
  - Authenticated vs unauthenticated requests.
  - Admin vs non-admin permissions.
  - Owner vs non-owner signups.
  - Valid vs invalid input.
- Run with:
  ```bash
  python manage.py test homepage
