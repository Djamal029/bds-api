"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class ActivityRegistrationDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def count(self, activity_id: uuid.UUID) -> int:
            stmt = (
                select(func.count())
                .select_from(ActivityRegistration)
                .where(ActivityRegistration.activity_id == activity_id)
            )
            return self._db.execute(stmt).scalar_one()

        def is_registered(self, activity_id: uuid.UUID, user_id: uuid.UUID) -> bool:
            stmt = select(ActivityRegistration).where(
                ActivityRegistration.activity_id == activity_id,
                ActivityRegistration.user_id == user_id,
            )
            return self._db.execute(stmt).scalar_one_or_none() is not None

        def register(
            self, activity_id: uuid.UUID, user_id: uuid.UUID
        ) -> ActivityRegistration:
            registration = ActivityRegistration(activity_id=activity_id, user_id=user_id)
            self._db.add(registration)
            self._db.flush()
            return registration

EXERCISE FOR CONTRIBUTORS, once you build this for real: registering
for a spots-limited activity has a genuine race condition — two people
registering for the last spot at the same instant can both pass a
plain `count() < max_spots` check before either commits, over-booking
the activity. The fix is a `SELECT ... FOR UPDATE` locking read on the
Activity row (see `Session.execute(select(...).with_for_update())`)
held for the whole registration, not just a plain count — this is a
real concurrency bug this exact codebase has hit and fixed before, so
it's worth building the locking version from the start rather than
discovering the race later under load.
"""
