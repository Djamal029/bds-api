"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class ActivityPaymentService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = ActivityPaymentDAO(db)
            self._notifications = NotificationService(db)

        def validate(self, due_id: uuid.UUID) -> ActivityPaymentDue:
            due = self._dao.lock_due(due_id)   # see that DAO stub's WHY note
            if due is None or due.status != PaymentStatusEnum.PENDING:
                raise PaymentNotPendingError(...)
            due.status = PaymentStatusEnum.VALIDATED
            self._notifications.notify(..., "Payment validated", ...)
            self._db.commit()   # AFTER notify(), so both land in one commit
            return due

The order in the sketch above matters: call `notify()` BEFORE
`commit()`, not after — `notify()` only flushes (see
dao/notification_dao.py's stub), so if you committed first, the
notification's `add()` would still be pending when the request ends
and get silently lost, the exact class of bug documented in
services/auth_service.py's module docstring, just with a different
missing-commit victim (a notification instead of a failed-login
counter).
"""
