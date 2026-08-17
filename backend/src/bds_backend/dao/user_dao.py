"""Database access for User/Member/Administrator.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY every write method here ends with `self._db.flush()`, never
`self._db.commit()`: flush sends the pending SQL to the database (so an
inserted row gets its generated defaults, like the UUID primary key,
immediately available on the Python object) without ending the
transaction. Only the SERVICE that called this DAO method decides when
the whole operation is actually done and calls `commit()`. See
services/auth_service.py's module docstring for the full reasoning and
a real bug this exact distinction prevents.

If you're tempted to add `self._db.commit()` to a DAO method "just to
be safe" — don't. It silently breaks any service method that composes
multiple DAO calls into one atomic operation (a very easy mistake:
a real bug in the actual BDS project had `AuthService.authenticate()`
recording a failed login attempt via a DAO call, then raising an
exception before anything committed — with a same-method commit it
would have worked, but the moment that DAO call's commit was correctly
removed in favor of service-level commits, the missing service-level
commit before the `raise` caused the failed-attempt count to be
silently lost on every wrong password, since closing a session with a
pending, uncommitted transaction rolls it back).

WHY `get_by_email_ci` exists alongside a plain `get_by_email`: SQL
string equality is case-sensitive on some engines/collations and not on
others — relying on that being "case-insensitive by default" is exactly
the kind of engine-specific behavior this project's "keep the ORM
portable" principle warns against (see README's SQLite-vs-MySQL note).
`func.lower(...)` makes the comparison explicitly, portably
case-insensitive regardless of the underlying engine's default
collation.
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from bds_backend.models.user import Member, User


class UserDAO:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_email_ci(self, email: str) -> User | None:
        stmt = select(User).where(func.lower(User.email) == email.lower())
        return self._db.execute(stmt).scalar_one_or_none()

    def get_by_username_ci(self, username: str) -> User | None:
        stmt = select(User).where(func.lower(User.username) == username.lower())
        return self._db.execute(stmt).scalar_one_or_none()

    def create_member(self, member: Member) -> Member:
        self._db.add(member)
        self._db.flush()
        return member

    def record_failed_login(self, user: User) -> None:
        user.failed_login_attempts += 1
        self._db.flush()

    def reset_failed_attempts(self, user: User) -> None:
        user.failed_login_attempts = 0
        self._db.flush()

    def set_session(self, user: User, session_id: str | None) -> None:
        user.current_session_id = session_id
        self._db.flush()

    def update_profile(self, user: User, **fields: object) -> User:
        for key, value in fields.items():
            if value is not None:
                setattr(user, key, value)
        self._db.flush()
        return user

    def rollback(self) -> None:
        """Not a commit-boundary violation: rolling back undoes a failed
        write attempt entirely (e.g. after a unique-constraint violation),
        it doesn't persist anything, so it's safe for a DAO to call directly
        rather than asking its caller to."""
        self._db.rollback()
