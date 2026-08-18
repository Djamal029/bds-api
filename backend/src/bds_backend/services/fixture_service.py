"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class FixtureService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = FixtureDAO(db)

        def update_score(
            self, fixture_id: uuid.UUID, home_score: int, away_score: int, close: bool
        ) -> Fixture:
            self._dao.upsert_result(fixture_id, home_score, away_score)
            if close:
                # change the Fixture's own status to FINISHED here too —
                # both writes belong to the same commit below
                ...
            self._db.commit()
            return self._dao.get_by_id(fixture_id)

Score entry needs a permission check tighter than "any logged-in user"
but the exact role (a "score reporter" flag, in the real project) is
out of scope to fully re-derive here — see api/deps.py's `require_role`
for the general mechanism once you add a role/flag beyond plain
member/administrator.
"""
