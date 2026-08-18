"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class NotificationDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def create(
            self, user_id: uuid.UUID, title: str, body: str, link: str | None = None
        ) -> Notification:
            notification = Notification(user_id=user_id, title=title, body=body, link=link)
            self._db.add(notification)
            self._db.flush()
            return notification

        def unread_count(self, user_id: uuid.UUID) -> int:
            stmt = select(func.count()).where(
                Notification.user_id == user_id, Notification.is_read.is_(False)
            )
            return int(self._db.execute(stmt).scalar_one())

        def mark_read(self, notification: Notification) -> Notification:
            notification.is_read = True
            self._db.flush()
            return notification

See services/team_service.py's stub for why `create()` here flushing
(not committing) matters more than usual: this DAO's `create()` is
meant to be called from OTHER services as a reactive side effect (a
payment gets validated, so a notification gets created as part of that
same operation) — it must never independently commit, or it would
silently split one logical operation into two separate transactions.
"""
