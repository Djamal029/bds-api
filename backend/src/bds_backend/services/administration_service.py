"""STUB — not implemented. Copy the pattern from services/auth_service.py.

Exists specifically so `api/v1/administration.py` (also a stub) never
talks to `dao/user_dao.py` directly — every route, without exception,
goes through a service, even when that service is thin and mostly just
forwards to one DAO method plus a commit. Skipping the service "because
it's simple" is the one architectural shortcut this codebase
deliberately never takes, precisely because it's the shortcut most
likely to be taken by accident otherwise.

    class AdministrationService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = UserDAO(db)

        def update_status(self, user_id: uuid.UUID, is_active: bool) -> User | None:
            user = self._dao.set_active(user_id, is_active)
            if user is not None:
                self._db.commit()
            return user

        def change_role(self, user_id: uuid.UUID, new_role: RoleEnum) -> User | None:
            user = self._dao.change_role(user_id, new_role)
            if user is not None:
                self._db.commit()
            return user

`change_role` needs `dao/user_dao.py` extended with a `change_role`
method — moving a row between the joined-table-inheritance child tables
(see models/user.py's module docstring for why this can't be done by
just editing an attribute on a loaded object).
"""
