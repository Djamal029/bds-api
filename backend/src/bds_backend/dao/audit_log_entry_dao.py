"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class AuditLogEntryDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def log(
            self,
            user_id: uuid.UUID,
            action: str,
            entity: str,
            entity_id: uuid.UUID | None = None,
            details: str | None = None,
        ) -> AuditLogEntry:
            entry = AuditLogEntry(
                user_id=user_id, action=action, entity=entity,
                entity_id=entity_id, details=details,
            )
            self._db.add(entry)
            self._db.flush()
            return entry

        def list(self, limit: int = 200) -> list[tuple[AuditLogEntry, str]]:
            \"\"\"Joined with the acting user's email so the admin UI doesn't
            need a second request per row just to show who did what.\"\"\"
            stmt = (
                select(AuditLogEntry, User.email)
                .join(User, User.id == AuditLogEntry.user_id)
                .order_by(AuditLogEntry.created_at.desc())
                .limit(limit)
            )
            return [(entry, email) for entry, email in self._db.execute(stmt).all()]

Unlike dao/notification_dao.py's `create()`, the SERVICE wrapping this
DAO (`services/audit_log_service.py`, also a stub) DOES commit right
after calling `log()` — an audit entry is written from a route as its
own standalone step, after whatever it's logging already committed
separately, not as a side effect inside that other operation's
transaction. See services/team_service.py's stub for that distinction
in more depth.
"""
