"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

router = APIRouter(prefix="/fixtures", tags=["fixtures"])

@router.get("/upcoming", response_model=list[FixtureRead])
def upcoming(
    db: Session = Depends(get_db), _user: User = Depends(get_current_user)
) -> list[Fixture]:
    return FixtureService(db).upcoming()

@router.put("/{fixture_id}/score", response_model=FixtureRead)
def update_score(
    fixture_id: uuid.UUID,
    payload: FixtureScoreUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),   # tighten to a reporter
                                                 # role once one exists
) -> Fixture:
    result = FixtureService(db).update_score(
        fixture_id, payload.home_score, payload.away_score, payload.close
    )
    AuditLogService(db).record(user.id, "update_score", "fixture", fixture_id)
    return result
"""
