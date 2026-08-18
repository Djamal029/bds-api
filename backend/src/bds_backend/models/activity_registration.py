"""STUB — not implemented. Copy the pattern from models/user.py.

One member's registration to one Activity — the join row between User
and Activity, and the row that ActivityPaymentDue (see
models/activity_payment.py) hangs off of.

    class ActivityRegistration(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "activity_registrations"

        activity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("activities.id"))
        user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

Add a unique constraint on `(activity_id, user_id)` so the same member
can't register twice for the same activity at the database level, not
just via an application-level pre-check (which, under concurrent
requests, is not by itself race-safe — see dao/user_dao.py's module
docstring for the general shape of this problem and how a database
constraint is the real guard, an app-level check is just a nicer error
message for the common case).
"""
