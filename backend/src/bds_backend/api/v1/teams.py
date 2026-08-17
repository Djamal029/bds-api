"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

You'll want at minimum:

    router = APIRouter(prefix="/teams", tags=["teams"])

    @router.get("", response_model=list[TeamRead])
    def list_teams(
        db: Session = Depends(get_db),
        _user: User = Depends(get_current_user),
    ) -> list[Team]:
        return TeamService(db).list_teams()

    @router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
    def create_team(
        data: TeamCreate,
        db: Session = Depends(get_db),
        _admin: User = Depends(require_admin),   # only admins can create
    ) -> Team:
        return TeamService(db).create_team(data)

Note the two different dependencies on the two routes above:
`get_current_user` (anyone logged in can list teams) vs `require_admin`
(only an administrator can create one) — see api/deps.py's `require_role`
for how that's built, and api/v1/auth.py's module docstring for why a
route should stay this thin (parse input, call one service method,
translate errors, return).

Once implemented, register it in api/v1/router.py (see that file's own
docstring for the exact line to add).
"""
