"""STUB — not implemented. Copy the pattern from models/user.py.

A `Sport` (e.g. "Football", "Basketball") is the top of the sports
hierarchy: a Sport has many Teams (see models/team.py, also a stub),
and a Team has many Players.

To implement, you need at minimum:

    class Sport(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "sports"

        name: Mapped[str] = mapped_column(String(100), unique=True)
        is_active: Mapped[bool] = mapped_column(Boolean, default=True)

Use `models/user.py` as your reference for:
  - the exact `Mapped`/`mapped_column` syntax
  - inheriting from `UUIDPrimaryKeyMixin` for the id column
  - `unique=True` for a column that must not repeat

Once implemented, don't forget:
  1. import it in `models/__init__.py` (or wherever models get imported
     so `Base.metadata` knows about the table — see db/session.py's
     docstring for why this matters)
  2. write a matching schemas/sports.py (see schemas/auth.py as a
     pattern for request/response Pydantic models)
  3. write dao/sport_dao.py (see dao/user_dao.py as a pattern)
  4. write services/sport_service.py (see services/auth_service.py —
     remember, the service owns the commit, the DAO only flushes)
  5. write api/v1/sports.py routes (see api/v1/auth.py as a pattern)
  6. add a test (see tests/test_auth.py as a pattern)
"""
