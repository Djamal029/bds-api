"""Reusable column groups shared across models, via multiple inheritance.

WORKED EXAMPLE — fully implemented, read this one closely.

This is the right place to understand `Mapped`/`mapped_column`, since
every other model in this project builds on these two mixins.

WHAT `Mapped[X]` means: it is a type annotation AND the actual runtime
type of the attribute once the class is instantiated. `Mapped[str]` means
"this column is a Python `str` when you read it, and SQLAlchemy will
validate/type-check that". `Mapped[str | None]` means the column is
nullable — the `| None` in the Python type IS what tells SQLAlchemy
(and mypy) that `None` is a legal value.

WHAT `mapped_column(...)` means: this is where you configure the actual
database column — its SQL type, whether it's a primary key, a default
value, a foreign key, etc. `Mapped[X]` says "what Python type do I get
back"; `mapped_column(...)` says "how is this actually stored".

WHY a UUID primary key instead of an auto-incrementing integer: integer
ids are guessable and sequential (user 42 tells you roughly how many
users existed before them, and an attacker can enumerate `/users/1`,
`/users/2`, ...). A random UUID carries no information and can't be
enumerated. The cost is a slightly larger index, which is an acceptable
trade for a small-to-medium application like this one.

WHY `default=uuid.uuid4` (a function reference) and not `default=uuid.uuid4()`
(a function call): the call form would generate ONE uuid when this module
is imported, and reuse that same value for every row ever created — a
catastrophic bug. The function reference tells SQLAlchemy "call this to
generate a fresh value for each new row".
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPrimaryKeyMixin:
    """Gives a model a random UUID primary key named `id`."""

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    """Gives a model a `created_at` column, set once at insert time.

    WHY `server_default` isn't used here in favor of a Python-side
    `default`: a Python default works identically across every database
    engine this project might run on (SQLite, MySQL, Postgres); a
    `server_default` would need engine-specific SQL (`CURRENT_TIMESTAMP`
    works everywhere, but more complex server defaults don't always
    translate) — another instance of the "keep the ORM portable" theme.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
