"""User accounts, using joined-table inheritance: `User` is the shared
base table, `Member` and `Administrator` each add their own columns in
their own tables, joined back to `users` on a shared primary key.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY joined-table inheritance instead of one flat `users` table with
nullable columns for both roles: a plain member never has an
`access_level`, and an administrator never has a `license_number` —
modeling that with nullable columns on one table means every row has
columns that are meaningless for it, and nothing stops a bug from
setting `access_level` on a member. Joined-table inheritance makes the
illegal state unrepresentable: a `Member` instance simply has no
`access_level` attribute to accidentally set.

The trade-off, and the thing that trips people up: SQLAlchemy cannot
change an existing row's `polymorphic_identity` (you cannot turn a
`Member` into an `Administrator` by just changing a Python attribute on
the loaded object) — promoting someone requires deleting the row from
one child table and inserting it into the other, keeping the same `id`.
That is a real operation this skeleton does not implement — it is
exactly the kind of thing a stub elsewhere in this codebase would point
you back to this comment for.

WHY `role` lives on the base `User` table (not inferred from which
child table a row is in): the JWT's `role` claim and every permission
check need to read the role without knowing which child table to join
against — a plain column read is far cheaper than "try both child
tables and see which one has a matching row".
"""

import enum
import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from bds_backend.db.base import Base
from bds_backend.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class RoleEnum(enum.StrEnum):
    MEMBER = "member"
    ADMINISTRATOR = "administrator"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Base table: every account, regardless of role, has these columns."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    username: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)

    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Account-lockout state (see services/auth_service.py for the flow
    # that reads and writes these): incremented on every wrong password,
    # reset to 0 on a successful login.
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)

    # See core/security.py's module docstring for why this exists: it is
    # what makes "only one active session per account" enforceable.
    current_session_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "role",
    }


class Member(User):
    """A regular member: can browse content, register for activities, and
    (if separately linked, out of scope for this skeleton) be a player.
    """

    __tablename__ = "members"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    __mapper_args__ = {"polymorphic_identity": RoleEnum.MEMBER}


class Administrator(User):
    """An administrator: manages content and other accounts. See the real
    project's `require_admin`/`require_super_admin` dependencies in
    api/deps.py for how this role gates access to write endpoints —
    reproduce that pattern here once you add administrator-only routes.
    """

    __tablename__ = "administrators"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    access_level: Mapped[str] = mapped_column(String(20), default="standard")

    __mapper_args__ = {"polymorphic_identity": RoleEnum.ADMINISTRATOR}
