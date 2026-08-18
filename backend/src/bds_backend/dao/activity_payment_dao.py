"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class ActivityPaymentDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def create_for_installment(
            self, registration_id: uuid.UUID, installment_id: uuid.UUID
        ) -> ActivityPaymentDue:
            due = ActivityPaymentDue(
                registration_id=registration_id, installment_id=installment_id
            )
            self._db.add(due)
            return due   # flush happens once, at the end of the batch — see
                          # the WHY note below

        def lock_due(self, due_id: uuid.UUID) -> ActivityPaymentDue | None:
            \"\"\"Locks the row (`SELECT ... FOR UPDATE`) before a status
            check in a treasurer validate/reject flow, so two concurrent
            reviews of the same due can't both read PENDING and both apply
            their outcome — see dao/activity_registration_dao.py's stub for
            the same race-condition shape applied to registration counts.\"\"\"
            stmt = select(ActivityPaymentDue).where(
                ActivityPaymentDue.id == due_id
            ).with_for_update()
            return self._db.execute(stmt).scalar_one_or_none()

WHY `create_for_installment` doesn't flush immediately, unlike most
other DAO `create` methods: when a member registers for an activity
with several installments, the calling service creates one due per
installment in a loop — flushing after every single one is wasted work
when one flush after the whole loop achieves the same result. This is
a deliberate exception to "every write flushes immediately", made by
the DAO author because the caller's usage pattern is known — the
service still owns the eventual `commit()` either way.
"""
