# Django Queue API Backend 

## Overview
This project is a Django REST Framework backend for managing coding practice sessions and signups.
It provides JWT authentication, custom user accounts, strict permissions, automated tests, and
self-documenting API docs via OpenAPI/Swagger. You can set it up via Docket.

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

  
### 8. Setup Guide

Clone and Installgit clone [github.com/amirdaniali/DSA_CYC_Interview:git](https://github.com/amirdaniali/DSA_CYC_Interview.git) 

You can use [uv](https://docs.astral.sh/uv/) to create a dedicated virtual environment.

```bash
cd backend
uv -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows 
uv pip install -r requirements.txt

```

To use PIP instead, create a new virtual environment and then install all packages hosted in `requirements.txt`. Run `migrate` to configure the initial database. and `createsuperuser` to create a new superuser account for accessing the admin. Execute the `runserver` command to start up the local server.

```
(.venv) $ pip install -r requirements.txt
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py runserver
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```


Then run `migrate` to configure the initial database. The command `createsuperuser` will create a new superuser account for accessing the admin. Execute the `runserver` command to start up the local server.

```
$ uv run manage.py migrate
$ uv run manage.py createsuperuser
$ uv run manage.py runserver
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```

Access

Admin: http://127.0.0.1:8000/admin/

API root: http://127.0.0.1:8000/api/

Swagger docs: http://127.0.0.1:8000/api/docs/swagger/

Redoc docs: http://127.0.0.1:8000/api/docs/redoc/


### DjangoX Features
- Django 5.1 & Python 3.13
- Installation via [uv](https://github.com/astral-sh/uv), [Pip](https://pypi.org/project/pip/) or [Docker](https://www.docker.com/)
- User authentication--log in, sign up, password reset--via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v5](https://getbootstrap.com/)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Custom 404, 500, and 403 error pages



### Docker

To use Docker with PostgreSQL as the database update the `DATABASES` section of `django_project/settings.py` to reflect the following:

```python
# django_project/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
```

The `INTERNAL_IPS` configuration in `django_project/settings.py` must be also be updated:

```python
# config/settings.py
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

And then proceed to build the Docker image, run the container, and execute the standard commands within Docker.

```
$ docker compose up -d --build
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```


