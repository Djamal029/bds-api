"""STUB — not implemented. Copy the pattern from models/user.py.

An immutable record of a sensitive action (who did what, to what, when)
— written by an administrator area's routes as a standalone step after
their main operation already committed (unlike Notification, this is
NOT called as a side effect inside another service's transaction, it's
its own independent unit of work — see services/team_service.py's stub
for that distinction).

    class AuditLogEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "audit_log_entries"

        user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
        action: Mapped[str] = mapped_column(String(50))      # e.g. "change_role"
        entity: Mapped[str] = mapped_column(String(50))      # e.g. "user"
        entity_id: Mapped[uuid.UUID | None] = mapped_column(
            Uuid(as_uuid=True), nullable=True
        )
        details: Mapped[str | None] = mapped_column(String(500), nullable=True)

Never expose a route that lets a client delete or edit a row in this
table — it exists to be trustworthy precisely because nothing (not even
an administrator, through the normal API) can rewrite history in it.
"""
