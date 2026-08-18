"""STUB — not implemented. Copy the pattern from models/user.py.

An in-app notification for one user, created as a reactive side effect
of some other operation (a payment being validated, a registration
succeeding) — see services/team_service.py's stub for the general
"a service can call another service as a side effect, but the CALLER
still owns the single commit" note, which is exactly how notifications
get created in the real project: the notification service's `notify()`
only ever flushes, never commits, because it's always called from
inside some other service's already-open unit of work.

    class Notification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "notifications"

        user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
        title: Mapped[str] = mapped_column(String(150))
        body: Mapped[str] = mapped_column(String(500))
        link: Mapped[str | None] = mapped_column(String(255), nullable=True)
        is_read: Mapped[bool] = mapped_column(Boolean, default=False)
"""
