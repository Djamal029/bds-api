"""STUB — not implemented. Copy the pattern from services/auth_service.py.
Read this one before implementing any OTHER service, though — it's the
key exception to "a service always ends with its own commit".

    class NotificationService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = NotificationDAO(db)

        def notify(
            self, user_id: uuid.UUID, title: str, body: str, link: str | None = None
        ) -> Notification:
            \"\"\"Flushes but deliberately does NOT commit — this is always
            called from another service as a reactive side effect (a
            payment gets validated, a registration succeeds), and that
            OTHER service owns the one commit for the whole operation. If
            this committed on its own, it would silently split one logical
            operation into two separate transactions — see
            services/activity_payment_service.py's stub for a concrete
            example of the ordering this requires (notify BEFORE commit,
            not after).\"\"\"
            return self._dao.create(user_id, title, body, link)

        def mark_read(self, user_id: uuid.UUID, notification_id: uuid.UUID) -> Notification:
            \"\"\"Unlike notify(), THIS method IS its own complete unit of
            work — a user marking their own notification read, called
            directly from a route, nothing else. It commits.\"\"\"
            notification = self._dao.get_by_id(notification_id)
            if notification is None or notification.user_id != user_id:
                raise NotificationForbiddenError(...)
            marked = self._dao.mark_read(notification)
            self._db.commit()
            return marked

Two methods on the same service, two different commit rules, both
correct: the difference is whether the method IS the whole operation
(`mark_read`) or is a STEP inside some other service's operation
(`notify`). Always ask which one you're writing before deciding whether
to commit.
"""
