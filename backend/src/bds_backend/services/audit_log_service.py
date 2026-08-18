"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class AuditLogService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = AuditLogEntryDAO(db)

        def record(
            self,
            user_id: uuid.UUID,
            action: str,
            entity: str,
            entity_id: uuid.UUID | None = None,
            details: str | None = None,
        ) -> None:
            \"\"\"Called from a ROUTE, as a standalone step after the main
            operation already committed on its own — this is its own
            complete unit of work, so unlike notification_service.py's
            `notify()`, this DOES commit.\"\"\"
            self._dao.log(user_id, action, entity, entity_id, details)
            self._db.commit()

        def list(self, limit: int = 200) -> list[AuditLogEntryRead]:
            return [
                AuditLogEntryRead(id=e.id, user_email=email, action=e.action, ...)
                for e, email in self._dao.list(limit)
            ]

A typical route calling this looks like:

    # commits itself:
    activity = ActivityService(db).create(data, admin.id)
    # ALSO commits itself, separately:
    AuditLogService(db).record(admin.id, "create", "activity", activity.id)

Two separate commits, deliberately — see the AuditLogEntryDAO stub for
why this one doesn't join the first operation's transaction.
"""
