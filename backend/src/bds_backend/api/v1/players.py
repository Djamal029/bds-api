"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/players", tags=["players"])

    @router.post("/{player_id}/generate-code", response_model=RegistrationCodeRead)
    def generate_code(
        player_id: uuid.UUID,
        db: Session = Depends(get_db),
        _admin: User = Depends(require_admin),
    ) -> RegistrationCode:
        return RecruitmentService(db).generate_code(player_id)

    @router.post("/become-player", response_model=PlayerRead, status_code=201)
    def become_player(
        data: BecomePlayerRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> Player:
        try:
            return RecruitmentService(db).become_player(user.id, data.code)
        except InvalidCodeError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/me", response_model=PlayerRead)
    def my_stats(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ) -> Player:
        player = RecruitmentService(db).my_stats(user.id)
        if player is None:
            raise HTTPException(status_code=404, detail="Not a player")
        return player

Still routed through a service, not `PlayerDAO(db)` called directly from
here — see api/v1/administration.py's stub for why that's true even for
a read this simple: consistency is the point (every route calls a
service, full stop), not "is this specific case complicated enough to
need one".
"""
