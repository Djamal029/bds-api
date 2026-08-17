"""Password hashing and JWT access/refresh tokens.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY hashing lives here and not in a model or DAO: hashing is a pure
cryptographic operation with no database dependency. Keeping it in
`core/` (infrastructure, not business logic) means `services/auth_service.py`
can call `hash_password()`/`verify_password()` without needing to know or
care which hashing algorithm is used underneath — swapping bcrypt for
argon2 later only touches this one file.

WHY two token types (access + refresh) instead of one long-lived token:
the access token is short-lived (see Settings.access_token_expire_minutes)
so a stolen token has a small window of use. The refresh token is
long-lived but can only be used at `POST /auth/refresh` to mint a new
access token — it is never accepted on any other endpoint, enforced by
the `type` claim checked in `decode_token()` below.

WHY a `sid` (session id) claim: this is what makes "only one active
session per account" possible. Every login writes a new random session
id onto both the user's row (`User.current_session_id`) and the issued
tokens. `api/deps.py`'s `get_current_user()` rejects any token whose
`sid` doesn't match the user's *current* session id — so logging in
elsewhere silently invalidates every previously issued token for that
account, without needing a token blocklist.
"""

import enum
import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from bds_backend.core.config import get_settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return str(_pwd_context.hash(plain_password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bool(_pwd_context.verify(plain_password, hashed_password))


class TokenType(enum.StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class InvalidTokenError(Exception):
    pass


def _create_token(subject: str, role: str, session_id: str, token_type: TokenType) -> str:
    settings = get_settings()
    expire_minutes = (
        settings.access_token_expire_minutes
        if token_type == TokenType.ACCESS
        else settings.refresh_token_expire_minutes
    )
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "role": role,
        "sid": session_id,
        "type": token_type.value,
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }
    return str(jwt.encode(payload, settings.secret_key, algorithm="HS256"))


def create_access_token(subject: str, role: str, session_id: str) -> str:
    return _create_token(subject, role, session_id, TokenType.ACCESS)


def create_refresh_token(subject: str, role: str, session_id: str) -> str:
    return _create_token(subject, role, session_id, TokenType.REFRESH)


def decode_token(token: str, expected_type: TokenType) -> dict[str, str]:
    """Raises InvalidTokenError for anything wrong with the token: expired,
    malformed, wrong signature, or the wrong `type` claim (e.g. someone
    trying to use a refresh token where an access token is expected).
    Deliberately a single error type/message for every failure mode — see
    the WHY note in dao/user_dao.py about not leaking which check failed.
    """
    settings = get_settings()
    try:
        payload: dict[str, str] = jwt.decode(
            token, settings.secret_key, algorithms=["HS256"]
        )
    except JWTError as exc:
        raise InvalidTokenError("Could not validate token") from exc

    if payload.get("type") != expected_type.value:
        raise InvalidTokenError("Wrong token type")

    return payload


def new_session_id() -> str:
    return str(uuid.uuid4())
