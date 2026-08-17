# Demo accounts

This skeleton ships one working feature (registration and login), so
there is no pre-seeded demo data — create an account yourself:

```bash
cd backend
uv run uvicorn bds_backend.main:app --reload
```

Then, against `http://localhost:8000/docs` (or any HTTP client):

```
POST /api/v1/auth/register
{ "email": "you@example.com", "password": "a-password-8-chars-min" }

POST /api/v1/auth/login
{ "email": "you@example.com", "password": "a-password-8-chars-min" }
```

The login response's `access_token` is what you pass as
`Authorization: Bearer <token>` to `GET /api/v1/auth/me` and
`PATCH /api/v1/auth/me`.

## Creating an administrator account

There is no admin-specific route in this skeleton (see
`api/v1/teams.py`'s stub for the pattern to follow once you add
administrator-only routes). To create one directly against the
database for testing:

```bash
cd backend
uv run python -c "
from bds_backend.db.session import SessionLocal
from bds_backend.models.user import Administrator, RoleEnum
from bds_backend.core.security import hash_password

db = SessionLocal()
db.add(Administrator(
    email='admin@example.com',
    password_hash=hash_password('AdminPassword123!'),
    role=RoleEnum.ADMINISTRATOR,
    username='admin',
))
db.commit()
"
```

## Regenerating the database from scratch

```bash
cd backend
rm -f dev.db
uv run python scripts/bootstrap_sqlite_dev.py
```

There is no `seed_demo.py` in this skeleton (unlike the real BDS
project) — this repo has no teams/fixtures/activities models
implemented yet, only accounts. Add one once you've implemented those
models, following the real project's `scripts/seed_demo.py` as a
pattern once you have access to it.
