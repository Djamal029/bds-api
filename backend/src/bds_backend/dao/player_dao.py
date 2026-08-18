"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class PlayerDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def get_by_id(self, player_id: uuid.UUID) -> Player | None:
            return self._db.get(Player, player_id)

        def get_by_user(self, user_id: uuid.UUID) -> Player | None:
            stmt = select(Player).where(Player.user_id == user_id)
            return self._db.execute(stmt).scalar_one_or_none()

        def link_to_user(self, player: Player, user_id: uuid.UUID) -> None:
            player.user_id = user_id
            self._db.flush()

        def create(self, team_id: uuid.UUID, last_name: str, first_name: str) -> Player:
            player = Player(team_id=team_id, last_name=last_name, first_name=first_name)
            self._db.add(player)
            self._db.flush()
            return player

A search-by-name method (`search(self, term: str) -> list[Player]`)
would use `Player.last_name.ilike(f"%{term}%")` — `ilike`, not `like`,
for a case-insensitive partial match, portable across SQLite/MySQL/
Postgres (see dao/user_dao.py's `get_by_email_ci` for the same
case-insensitivity concern solved a different way, with `func.lower`,
which is the right tool for an exact match rather than a partial one).
"""
