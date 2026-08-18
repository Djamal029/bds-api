"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class RecruitmentService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._codes = RegistrationCodeDAO(db)
            self._players = PlayerDAO(db)

        def become_player(self, user_id: uuid.UUID, code: str) -> Player:
            registration_code = self._codes.get_by_code(code)
            if registration_code is None or registration_code.used:
                raise InvalidCodeError(...)
            if registration_code.expiration_date < datetime.now(UTC):
                raise InvalidCodeError(...)
            player = self._players.get_by_id(registration_code.player_id)
            self._players.link_to_user(player, user_id)
            self._codes.mark_used(registration_code, datetime.now(UTC))
            self._db.commit()   # linking the player AND marking the code
                                 # used happen together, or neither does
            return player

        def generate_code(self, player_id: uuid.UUID) -> RegistrationCode:
            code = "".join(secrets.choice(ALPHABET) for _ in range(8))
            registration_code = RegistrationCode(
                code=code, player_id=player_id,
                expiration_date=datetime.now(UTC) + timedelta(days=7),
            )
            created = self._codes.create(registration_code)
            self._db.commit()
            return created

`become_player`'s two writes (`link_to_user`, `mark_used`) committing
together is exactly the point of this whole convention: if only one of
them persisted, the system would end up in an impossible state (a
player linked to an account whose code still shows as unused, or vice
versa) — a bug a database can't catch for you, only correct
transaction boundaries can.
"""
