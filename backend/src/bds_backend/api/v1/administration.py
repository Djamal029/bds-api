"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/administration", tags=["administration"])

    @router.get("/users", response_model=list[UserRead])
    def list_users(
        db: Session = Depends(get_db), _user: User = Depends(require_admin)
    ) -> list[User]:
        return AdministrationService(db).list_users()

    @router.patch("/users/{user_id}/status", response_model=UserRead)
    def update_status(
        user_id: uuid.UUID,
        payload: AccountStatusUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin),
    ) -> User:
        if user_id == current_user.id and not payload.is_active:
            raise HTTPException(status_code=400, detail="Cannot disable your own account")
        service = AdministrationService(db)
        user = service.update_status(user_id, payload.is_active)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        action = "activate" if payload.is_active else "deactivate"
        AuditLogService(db).record(current_user.id, action, "user", user_id)
        return user

Notice the self-modification guard (`user_id == current_user.id`)
BEFORE calling the service — a permission/sanity check that only needs
the caller's own id, not a database read, belongs in the route, cheap
and early; a check needing a database read (does the target account
exist, what role does it have) belongs in the service.
"""
