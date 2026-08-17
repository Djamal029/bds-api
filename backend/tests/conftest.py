"""Shared pytest fixtures: an isolated in-memory SQLite database per test,
and a FastAPI TestClient wired to use it instead of the real database.

WORKED EXAMPLE — fully implemented.

WHY `:memory:` SQLite for tests instead of the real `dev.db` file (or a
real MySQL database): tests must be fast, isolated from each other, and
safe to run in any order or in parallel — a fresh in-memory database per
test, torn down immediately after, guarantees one test's data can never
leak into or interfere with another's.

WHY `app.dependency_overrides[get_db] = _override_get_db`: this is
FastAPI's built-in mechanism for swapping a dependency at test time
without changing any application code — every route that depends on
`get_db` (directly, or via other dependencies like `get_current_user`
that themselves depend on it) transparently receives the test session
instead of a real one.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from bds_backend.api.deps import get_db
from bds_backend.db.base import Base
from bds_backend.main import create_app
from bds_backend.models import *  # noqa: F401,F403  (registers every model)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def _override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
