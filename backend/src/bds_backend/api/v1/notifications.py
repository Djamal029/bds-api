"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/notifications", tags=["notifications"])

    @router.get("", response_model=list[NotificationRead])
    def list_mine(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ) -> list[Notification]:
        return NotificationService(db).list_for_user(user.id)

    @router.get("/unread-count", response_model=UnreadCountRead)
    def unread_count(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ) -> UnreadCountRead:
        count = NotificationService(db).unread_count(user.id)
        return UnreadCountRead(count=count)

    @router.post("/{notification_id}/read", response_model=NotificationRead)
    def mark_read(
        notification_id: uuid.UUID,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> Notification:
        try:
            return NotificationService(db).mark_read(user.id, notification_id)
        except NotificationForbiddenError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc

`mark_read`'s 403 (not 404) when the notification belongs to someone
else: revealing "exists but isn't yours" vs "doesn't exist" as
different responses would let a client enumerate other users'
notification ids by id-guessing and watching which status code comes
back — see services/auth_service.py's `authenticate()` docstring for
the same enumeration-prevention idea applied to login.
"""
