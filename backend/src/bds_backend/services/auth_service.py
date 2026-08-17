"""Business orchestration for authentication.

WORKED EXAMPLE — fully implemented. THIS IS THE FILE TO READ FIRST to
understand where database commits belong in this codebase.

THE RULE: a DAO method flushes; a SERVICE method commits, exactly once,
covering everything that logically belongs to one operation. The
service is the layer that knows what "one operation" means — a DAO
method only knows about one table, it cannot know whether it's being
called alone or as step 2 of 3 in some larger unit of work.

A REAL BUG THIS PREVENTS (this actually happened in the real BDS
project this skeleton is modeled on): `authenticate()` below, on a
wrong password, records a failed-login attempt and then raises
`InvalidCredentialsError`. The very first version of this service
called a DAO method that committed internally. That worked, by
accident. When commits were correctly moved out of DAOs and into
services (the change this whole file is demonstrating), the service
method still just raised the exception immediately after the DAO call,
with no commit in between. The DAO call had flushed the failed-attempt
increment (so it was visible within the transaction), but nothing had
committed it — and when the request finished and FastAPI's `get_db()`
dependency closed the session (see db/session.py), a session with a
pending uncommitted transaction rolls it back on close. The failed
login counter silently reset to nothing on every wrong password,
quietly breaking account lockout. The fix is visible below: `self._db
.commit()` runs BEFORE the `raise`, not after — you cannot run code
after a raise, so the commit has to come first, and it is easy to
forget that when a method's normal flow is "do the write, then bail
out with an error".

THE GENERAL PATTERN to copy for every other service you write:
  1. Do all your reads and validation first (raise early, before any
     write, whenever you can — cheaper to fail before touching the DB).
  2. Call whichever DAO methods this operation needs. Each one flushes,
     none of them commit.
  3. Call `self._db.commit()` exactly once, as the LAST thing that
     happens on every path that should actually persist something —
     including paths that end in a raise, if a write happened on that
     path (see `authenticate()`'s wrong-password branch below).
  4. A path that raises WITHOUT having written anything needs no commit
     at all — there's nothing to make durable.
"""

import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bds_backend.core.config import get_settings
from bds_backend.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    new_session_id,
    verify_password,
)
from bds_backend.dao.user_dao import UserDAO
from bds_backend.models.user import Member, RoleEnum, User
from bds_backend.schemas.auth import MemberRegistration, ProfileUpdate, TokenPair


class EmailAlreadyUsedError(Exception):
    pass


class UsernameAlreadyUsedError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class AuthService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._dao = UserDAO(db)
        self._settings = get_settings()

    def register_member(self, data: MemberRegistration) -> Member:
        if self._dao.get_by_email(data.email) is not None:
            raise EmailAlreadyUsedError(f"Email already in use: {data.email}")

        member = Member(
            email=data.email,
            password_hash=hash_password(data.password),
            role=RoleEnum.MEMBER,
        )
        try:
            created = self._dao.create_member(member)
            self._db.commit()  # the whole registration succeeds as one unit
            return created
        except IntegrityError as exc:
            # Two concurrent registrations for the same email can both
            # pass the get_by_email() check above before either commits:
            # the database's unique constraint on users.email is the real
            # guard against a duplicate account, this is just a backstop
            # that turns the resulting IntegrityError into the same
            # domain error the pre-check raises, instead of a raw 500.
            self._dao.rollback()
            raise EmailAlreadyUsedError(f"Email already in use: {data.email}") from exc

    def authenticate(self, email: str, password: str) -> User:
        """Raises InvalidCredentialsError for both "no such account" and
        "wrong password" — deliberately the same message and exception for
        both, so a client cannot tell which one happened. If they were
        distinguishable, an attacker could enumerate valid email addresses
        by testing them one at a time and watching which error came back.
        """
        user = self._dao.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Incorrect email or password")

        if not verify_password(password, user.password_hash):
            # EXERCISE FOR CONTRIBUTORS: once `failed_login_attempts`
            # reaches `self._settings.failed_login_max_attempts`, lock the
            # account (add a `locked_until: Mapped[datetime | None]` column
            # to User, set it here, and check it at the top of this method
            # before the password check runs at all).
            self._dao.record_failed_login(user)
            # See this file's module docstring: commit BEFORE raising, or
            # the increment above is silently lost when the session closes.
            self._db.commit()
            raise InvalidCredentialsError("Incorrect email or password")

        if not user.is_active:
            raise InvalidCredentialsError("Account disabled")

        self._dao.reset_failed_attempts(user)
        self._db.commit()
        return user

    def open_session(self, user: User) -> TokenPair:
        """Issues a new token pair and a new session id: only one active
        session per account, so logging in again from anywhere implicitly
        invalidates whatever token was issued last time (see
        core/security.py's module docstring for how the `sid` claim makes
        that enforceable)."""
        session_id = new_session_id()
        self._dao.set_session(user, session_id)
        self._db.commit()
        return TokenPair(
            access_token=create_access_token(str(user.id), user.role.value, session_id),
            refresh_token=create_refresh_token(str(user.id), user.role.value, session_id),
        )

    def update_profile(self, user: User, data: ProfileUpdate) -> User:
        if data.username is not None:
            existing = self._dao.get_by_username_ci(data.username)
            if existing is not None and existing.id != user.id:
                raise UsernameAlreadyUsedError(f"Username already taken: {data.username}")

        member_fields: dict[str, object] = {}
        if isinstance(user, Member):
            member_fields = {"first_name": data.first_name, "last_name": data.last_name}

        try:
            updated = self._dao.update_profile(
                user, username=data.username, **member_fields
            )
            self._db.commit()
            return updated
        except IntegrityError as exc:
            self._dao.rollback()
            raise UsernameAlreadyUsedError(
                f"Username already taken: {data.username}"
            ) from exc


def parse_user_id(raw: str) -> uuid.UUID | None:
    """Small helper used by api/deps.py — a malformed id in a token's
    `sub` claim should look exactly like "user not found" to the caller,
    not raise an unhandled ValueError."""
    try:
        return uuid.UUID(raw)
    except ValueError:
        return None
