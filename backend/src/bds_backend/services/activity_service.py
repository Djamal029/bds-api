"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class ActivityService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = ActivityDAO(db)
            self._registrations = ActivityRegistrationDAO(db)
            self._payments = ActivityPaymentDAO(db)
            self._notifications = NotificationService(db)

        def register(self, activity_id: uuid.UUID, user_id: uuid.UUID) -> None:
            # 1. lock and re-check spots remaining (see
            #    dao/activity_registration_dao.py's stub for the race
            #    condition this must guard against)
            # 2. create the registration
            # 3. create one ActivityPaymentDue per installment, plus one for
            #    the deposit if the activity has one
            # 4. notify the member a payment is due, if any was created
            # 5. ONE self._db.commit() at the end, covering all of the above
            ...

This is the service with the most moving parts to get right in this
whole skeleton once you build it: read services/auth_service.py's
module docstring again before starting, specifically the point about
committing every write that belongs to one logical operation together,
exactly once. A registration, its payment dues, and its notification
are one operation, not three.
"""
