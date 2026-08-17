"""Shared FastAPI dependencies: getting a DB session, resolving the
current authenticated user, and role-gating a route.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY `get_current_user` re-checks the session id (`sid`) against the
user's `current_session_id` column on every single request, not just at
login: the token itself doesn't know if the user has since logged in
elsewhere (which rotates `current_session_id` to a new value, see
services/auth_service.py's `open_session()`). A token is only valid
proof of identity as long as it matches the account's CURRENT session —
checking this on every request is what actually enforces "only one
active session per account", not just at issue time.

WHY `require_role(...)` is a function that RETURNS a dependency function
(instead of being the dependency directly): it needs to be parameterized
per-route with which role(s) are allowed, and FastAPI dependencies are
just callables — `Depends(require_role(RoleEnum.ADMINISTRATOR))` calls
`require_role` once (at route-definition time) to produce the actual
dependency function FastAPI will call on every request.

WHY the 401 for "no such user"/"invalid session" and 403 for "wrong
role" are different status codes, and both are used deliberately: 401
means "I don't know who you are" (bad/expired/mismatched token) — the
client should try logging in again. 403 means "I know who you are, and
you're not allowed to do this" — logging in again won't help, the
account itself lacks permission.
"""

from collections.abc import Callable, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from bds_backend.core.security import InvalidTokenError, TokenType, decode_token
from bds_backend.dao.user_dao import UserDAO
from bds_backend.db.session import get_db as _get_db
from bds_backend.models.user import RoleEnum, User
from bds_backend.services.auth_service import parse_user_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    yield from _get_db()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token, TokenType.ACCESS)
    except InvalidTokenError as exc:
        raise credentials_error from exc

    user_id = parse_user_id(payload.get("sub", ""))
    if user_id is None:
        raise credentials_error

    user = UserDAO(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise credentials_error
    if user.current_session_id != payload.get("sid"):
        raise credentials_error

    return user


def require_role(*roles: RoleEnum) -> Callable[..., User]:
    def _dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for this role",
            )
        return user

    return _dependency


require_admin = require_role(RoleEnum.ADMINISTRATOR)
