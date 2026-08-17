"""Mounts every v1 router under one `/api/v1` prefix.

WORKED EXAMPLE — fully implemented.

WHY a separate router-aggregation file instead of registering each
router directly on the `FastAPI()` app in main.py: as more domains are
added (teams, fixtures, activities, ...), main.py should not need to
change — it only ever mounts `api_router` once. Adding a new domain
means adding one import and one `include_router(...)` call here, in one
place, not touching main.py's own setup.

When you implement api/v1/teams.py (see that file's stub for what it
needs), wire it in here:

    from bds_backend.api.v1 import teams
    api_router.include_router(teams.router)
"""

from fastapi import APIRouter

from bds_backend.api.v1 import auth

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
