"""The SQLAlchemy engine, session factory, and the `get_db` FastAPI
dependency every route depends on to receive a database session.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY the connection-pool settings branch on the URL scheme: SQLite is a
single local file with no real concurrent-connection concept, so pool
tuning is meaningless (and `check_same_thread=False` is required instead,
since FastAPI can hand a request to a different thread than the one that
opened the session). MySQL/Postgres are real network databases where the
pool size caps how many concurrent requests can talk to the database at
once — too small and requests queue and time out under load, too large
and you can exhaust the database server's own connection limit. This is
exactly the kind of thing that must be re-checked when the real project
moves off SQLite (see README's "why SQLite" note): the ORM makes the
*queries* portable for free, but pool tuning is not free, it is a
deliberate choice per engine.

WHY `get_db()` is a generator, not a plain function: FastAPI recognizes
generator dependencies and runs the code after the `yield` as cleanup,
guaranteed to run even if the route raises — so the session is always
closed, whether the request succeeded or failed.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from bds_backend.core.config import get_settings

settings = get_settings()

_is_sqlite = settings.database_url.startswith("sqlite")

_connect_args = {"check_same_thread": False} if _is_sqlite else {}
_pool_kwargs = (
    {} if _is_sqlite else {"pool_size": 20, "max_overflow": 40, "pool_pre_ping": True}
)

engine = create_engine(settings.database_url, connect_args=_connect_args, **_pool_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
