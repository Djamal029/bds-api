"""Create the SQLite schema directly from the ORM models.

WORKED EXAMPLE — fully implemented, and directly usable.

WHY this exists instead of Alembic migrations: this skeleton has no
migration history to replay (there's only ever one schema state, the
current one) — `Base.metadata.create_all(engine)` is exactly equivalent
to "create every table that doesn't already exist", which is all a
fresh setup needs. The real BDS project keeps Alembic migrations for
its MySQL production database (schema history matters once real data
exists), but even there, this same shortcut is used for local SQLite
development (see that project's CONTRIBUTING.md) because Alembic's
migration chain there contains MySQL-only DDL that cannot run against
SQLite at all.

Usage (from backend/):

    uv run python scripts/bootstrap_sqlite_dev.py
"""

from bds_backend.db.base import Base
from bds_backend.db.session import engine
from bds_backend.models import *  # noqa: F401,F403  (registers every model)


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("SQLite schema created.")


if __name__ == "__main__":
    main()
