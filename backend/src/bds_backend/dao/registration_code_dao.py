"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class RegistrationCodeDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def get_by_code(self, code: str) -> RegistrationCode | None:
            stmt = select(RegistrationCode).where(RegistrationCode.code == code)
            return self._db.execute(stmt).scalar_one_or_none()

        def mark_used(self, registration_code: RegistrationCode, used_at: datetime) -> None:
            registration_code.used = True
            registration_code.used_at = used_at
            self._db.flush()

        def create(self, registration_code: RegistrationCode) -> RegistrationCode:
            self._db.add(registration_code)
            self._db.flush()
            return registration_code

The service that calls `create()` is responsible for generating the
actual code string (random, unguessable — `secrets.choice(...)` over an
uppercase-letters-and-digits alphabet, never `random`, which is not
cryptographically secure and shouldn't be used for anything
security-sensitive like an access code).
"""
