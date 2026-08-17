# Contributing

This repository is an architecture skeleton for the BDS platform: it
teaches the pattern through one fully working feature (authentication)
and leaves everything else as a stub pointing back at that example. See
`README.md` for the layer diagram and how to run it, and
`Cahier_des_charges.md` for the product context.

## The rule every file in this skeleton follows

**A DAO method flushes. A service method commits, exactly once, for
its whole unit of work.**

This is not a style preference — `backend/src/bds_backend/services/
auth_service.py`'s module docstring documents a real bug this exact
rule prevents: a DAO call that used to commit on its own hid the fact
that a service method could raise an exception right after a write,
with nothing ever making that write durable. Read that file before
writing any service method of your own.

## Layer-by-layer, with the exact file to copy

| Layer | Worked example (read this) | Stub (copy the pattern into this) |
|---|---|---|
| Models | `models/mixins.py`, `models/user.py` | `models/sport.py`, `models/team.py` |
| Schemas | `schemas/auth.py` | `schemas/teams.py` |
| DAO | `dao/user_dao.py` | `dao/team_dao.py` |
| Service | `services/auth_service.py` | `services/team_service.py` |
| Routes | `api/v1/auth.py`, `api/deps.py` | `api/v1/teams.py` |
| Frontend API client | `frontend/src/api/client.ts`, `auth.ts` | (write `teams.ts` yourself) |
| Frontend screen | `frontend/src/screens/LoginScreen.tsx` | `frontend/src/screens/TeamsScreen.tsx` |

Every stub file has a docstring with the minimum code needed to get
started and a pointer to which worked example to model it on. None of
them are silently empty.

## Adding a whole new feature, step by step

Say you want to implement teams (the natural next step — see
`Cahier_des_charges.md`'s closing section). In order:

1. **Model** (`models/team.py`): fill in the `Team` class per its
   docstring. Add it to `models/__init__.py`'s imports.
2. **Schema** (`schemas/teams.py`): `TeamCreate` (request) and
   `TeamRead` (response) per its docstring, following `schemas/auth.py`
   for the request-vs-response split reasoning.
3. **DAO** (`dao/team_dao.py`): `get_by_id`, `list_by_sport`, `create`
   — ending every write method in `flush()`, never `commit()`.
4. **Service** (`services/team_service.py`): wraps the DAO, owns the
   one `commit()` per operation.
5. **Routes** (`api/v1/teams.py`): thin, following `api/v1/auth.py` —
   parse input via a schema, call one service method, translate any
   domain exception to an HTTP error, return.
6. **Wire it in** (`api/v1/router.py`): one import, one
   `include_router(...)` call.
7. **Frontend client** (`frontend/src/api/teams.ts`, new file): a
   `Team` interface matching `TeamRead` field for field, one function
   per route, following `api/auth.ts`.
8. **Frontend screen**: fill in `screens/TeamsScreen.tsx` per its
   docstring.
9. **Test** (`backend/tests/test_teams.py`, new file): at minimum, the
   happy path and one permission-boundary case (a non-admin rejected
   from creating a team), following `tests/test_auth.py`'s shape.

Run the full gate before considering it done:

```bash
cd backend
uv run ruff format . && uv run ruff check .
uv run mypy src
uv run pytest -q
cd ../frontend
npx tsc --noEmit
```

## Where Git commits happen

Not to be confused with the database-commit rule above — this is about
version control.

- Work on a feature branch (`git checkout -b add-teams`), never commit
  directly to `main`.
- One logical change per commit. If the commit message needs "and" to
  describe it, it is probably two commits.
- Imperative mood: "Add team creation endpoint", not "Added" or
  "Adding".
- Run the full gate (above) before every commit that's meant to be
  shared — a broken intermediate commit is fine locally, never push one.
- Open a pull request against `main` when a feature is complete and
  tested; describe *why* the change exists in the PR description, the
  diff already shows *what* changed.
