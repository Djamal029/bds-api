"""Authentication routes: register, login, read/update your own profile.

WORKED EXAMPLE — fully implemented. This is the one complete, working,
end-to-end feature in this skeleton — `POST /register`, `POST /login`,
`GET /me`, `PATCH /me` all actually work against a real (SQLite)
database, see README.md for how to run and try them.

WHY every route here is short (parse input via `Depends`, call exactly
one service method, translate its exceptions to HTTP errors, return):
a route's only job is to speak HTTP. It never contains a business rule
itself — "is this email already taken" lives in AuthService, not here.
That split is what makes the service layer testable without spinning up
FastAPI at all (see tests/test_auth.py).

WHY exceptions are translated here, in the route, rather than the
service raising an HTTPException directly: services/auth_service.py has
no FastAPI import anywhere in it — it's plain Python, raising plain
Python exceptions, which is what makes it independently unit-testable
and, in principle, reusable from a non-HTTP context (a CLI script, a
background job) without dragging a whole HTTP framework along.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from bds_backend.api.deps import get_current_user, get_db
from bds_backend.models.user import User
from bds_backend.schemas.auth import (
    LoginRequest,
    MemberRegistration,
    ProfileUpdate,
    TokenPair,
    UserRead,
)
from bds_backend.services.auth_service import (
    AuthService,
    EmailAlreadyUsedError,
    InvalidCredentialsError,
    UsernameAlreadyUsedError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: MemberRegistration, db: Session = Depends(get_db)) -> User:
    try:
        return AuthService(db).register_member(data)
    except EmailAlreadyUsedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=TokenPair)
def login(data: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    service = AuthService(db)
    try:
        user = service.authenticate(data.email, data.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc
    return service.open_session(user)


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)) -> User:
    return user


@router.patch("/me", response_model=UserRead)
def update_me(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> User:
    try:
        return AuthService(db).update_profile(user, data)
    except UsernameAlreadyUsedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
