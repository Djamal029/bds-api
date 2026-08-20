# BDS API — Architecture Skeleton

This repository is a **teaching skeleton**, not a runnable clone of the
full BDS product. It mirrors the real project's architecture (same
layer names, same file layout, same conventions) so two new
contributors can learn the pattern from real, working examples, then
build the rest themselves.

Every layer has **at least one fully implemented, heavily commented
example file**. Every other file in that layer is a **stub**: a real
class or function signature with a docstring explaining what it must
do and which example file to copy the pattern from, but no
implementation body. Nothing is silently empty — a stub always says
what belongs there and where to look.

## Why this exists

Reading a full production codebase cold is slow: the interesting
pattern (how a request flows from a route to the database and back) is
buried in hundreds of files. This skeleton isolates that pattern to a
handful of files built around one working feature — authentication
(register, login, read/update your own profile) — so it can be read
start to finish in one sitting.

## Architecture

Every request passes through the same five layers, always in this
order, each one only ever calling the layer directly below it:

```
Frontend screen (screens/*.tsx)
        |  calls a typed function
        v
Frontend API client (api/*.ts)
        |  HTTP request (axios)
        v
Backend route (api/v1/*.py)
        |  validates input against a schema, checks the caller's role
        v
Service (services/*.py)
        |  business rules, orchestrates one or more DAOs, OWNS COMMITS
        v
DAO (dao/*.py)
        |  builds and runs the SQL query, never commits
        v
Model (models/*.py)
        |  maps to a database table (SQLAlchemy Mapped columns)
```

### The rule that matters most: commits belong in services, not DAOs

A DAO method **flushes** (`db.flush()`) so the row exists and has its
generated id/defaults available within the current transaction, but it
**never commits**. The **service** method that called it decides when
the whole operation is done and calls `db.commit()` exactly once for
that unit of work.

Why this matters, concretely: `AuthService.register_member()` in this
skeleton calls two DAO methods and one notification helper before it
commits. If each of those committed on its own, a failure partway
through would leave a half-finished operation permanently saved —
a user record with no linked data, for example. One commit at the end
of the service method means the whole operation succeeds or fails as
one atomic unit. See `services/auth_service.py` for the real pattern,
including a documented real bug this exact mistake caused (a failed
login attempt being silently lost because the DAO's caller never
committed before raising an exception).

### Where Git commits happen

Unrelated to database commits above — this is about version control.

- Work on a feature branch, never directly on `main`.
- One logical change per commit: a commit message should be
  answerable in one sentence ("why did this change happen"), if it
  needs "and" to describe it, it is probably two commits.
- Before opening a pull request: `ruff format`, `ruff check`, `mypy`,
  and the test suite must all be clean (see below for the exact
  commands) — the same gate this skeleton's own example code already
  passes.
- Commit messages: imperative mood ("Add team roster endpoint", not
  "Added" or "Adding"), explain *why* in the body if the *why* is not
  obvious from the diff itself.

## Running it

This defaults to SQLite so no database server is required to start:

```bash
cd backend
uv sync
cp .env.example .env
uv run python scripts/bootstrap_sqlite_dev.py   # creates the schema
uv run uvicorn bds_backend.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API docs. Try
`POST /api/v1/auth/register`, then `POST /api/v1/auth/login`, then
`GET /api/v1/auth/me` with the returned access token — that is the one
complete, working, real feature this skeleton ships.

Run the checks:

```bash
uv run ruff format . && uv run ruff check --fix .
uv run mypy src
uv run pytest -q
```

## Where everything is

| Path | What it is |
|---|---|
| `backend/src/bds_backend/core/` | Settings, password hashing, JWT — infrastructure every layer depends on |
| `backend/src/bds_backend/db/` | SQLAlchemy engine/session setup |
| `backend/src/bds_backend/models/` | ORM table definitions |
| `backend/src/bds_backend/schemas/` | Pydantic request/response shapes |
| `backend/src/bds_backend/dao/` | Database queries |
| `backend/src/bds_backend/services/` | Business rules, commit ownership |
| `backend/src/bds_backend/api/` | FastAPI routes, permission checks |
| `frontend/src/api/` | Typed HTTP client functions, one module per backend domain |
| `frontend/src/screens/` | One file per screen |

See `CONTRIBUTING.md` for the file-by-file guide and a worked example
of adding a brand new feature through every layer.

See `DEMO_ACCOUNTS.md` for the seeded demo accounts and how to
regenerate them.

See `Cahier_des_charges.md` for the product-level scope this skeleton
is standing in for — what the real BDS platform does, so the
architecture choices here make sense in context — including the team's
build roadmap toward a full MVP, and `diagramme_classes_bds_api.html`
for the class diagram that roadmap builds toward.
