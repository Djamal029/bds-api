"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/activities", tags=["activities"])

    @router.get("", response_model=list[ActivityRead])
    def list_upcoming(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ) -> list[Activity]:
        return ActivityService(db).list_upcoming(user.id)

    @router.post("", response_model=ActivityRead, status_code=201)
    def create(
        data: ActivityCreate,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
    ) -> Activity:
        return ActivityService(db).create(data, admin.id)

    @router.post("/{activity_id}/registration", status_code=204)
    def register(
        activity_id: uuid.UUID,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> None:
        try:
            ActivityService(db).register(activity_id, user.id)
        except ActivityFullError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

Wire this into api/v1/router.py once implemented (see that file's own
docstring for the exact line to add).
"""
