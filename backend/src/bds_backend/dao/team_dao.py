"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

You'll want at minimum:

    class TeamDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def get_by_id(self, team_id: uuid.UUID) -> Team | None:
            return self._db.get(Team, team_id)

        def list_by_sport(self, sport_id: uuid.UUID) -> list[Team]:
            stmt = select(Team).where(Team.sport_id == sport_id)
            return list(self._db.execute(stmt).scalars().all())

        def create(self, team: Team) -> Team:
            self._db.add(team)
            self._db.flush()   # NOT commit() — see dao/user_dao.py's
                                # module docstring for why
            return team

Remember the one rule every DAO in this project follows without
exception: a DAO method ends with `flush()`, never `commit()`. The
service layer decides when an operation is complete.
"""
