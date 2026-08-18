"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class ActivityDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def get_by_id(self, activity_id: uuid.UUID) -> Activity | None:
            return self._db.get(Activity, activity_id)

        def list_upcoming(self, now: datetime, limit: int = 20) -> list[Activity]:
            stmt = (
                select(Activity)
                .where(Activity.date_time >= now)
                .order_by(Activity.date_time)
                .limit(limit)
                .options(selectinload(Activity.installments))   # see note below
            )
            return list(self._db.execute(stmt).scalars().all())

        def create(self, activity: Activity) -> Activity:
            self._db.add(activity)
            self._db.flush()   # NOT commit() — the service commits
            return activity

WHY `.options(selectinload(...))` on the list query: without it,
serializing N activities into a response that includes each one's
installments fires one extra query PER activity (N+1 queries) instead
of two queries total. This is a real, previously-fixed performance bug
in the project this skeleton is based on — always check whether a list
endpoint's response needs a related table, and eager-load it explicitly
if so, rather than relying on lazy loading.
"""
