"""FastAPI application factory.

WORKED EXAMPLE — fully implemented.

WHY a `create_app()` factory function instead of a bare module-level
`app = FastAPI()`: tests need a fresh app instance with the database
dependency overridden to point at a throwaway test database (see
tests/conftest.py) — a factory function makes that trivial
(`create_app()` inside the test fixture); a single module-level `app`
would force every test to share the same instance and the same
dependency wiring as the real running server.

WHY `allow_credentials=False` on CORS even though `allow_origins=["*"]`:
this app authenticates with a Bearer token in the `Authorization`
header, never with cookies — so it never needs the browser to send
credentials automatically, and combining a wildcard origin with
`allow_credentials=True` is a real vulnerability (browsers then reflect
the literal request Origin back instead of enforcing `*`, effectively
allowing any site to make credentialed requests). Since this app never
needs credentialed CORS requests at all, the safe fix is simply not to
turn that flag on.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bds_backend.api.v1.router import api_router
from bds_backend.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="BDS API (skeleton)")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()
