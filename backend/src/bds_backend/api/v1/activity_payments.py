"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/activity-payments", tags=["activity-payments"])

    @router.get("", response_model=list[ActivityPaymentDueRead])
    def list_all(
        db: Session = Depends(get_db), _user: User = Depends(require_admin)
    ) -> list[ActivityPaymentDueRead]:
        return ActivityPaymentService(db).list_all()

    @router.post("/{due_id}/validate", response_model=ActivityPaymentDueRead)
    def validate(
        due_id: uuid.UUID,
        db: Session = Depends(get_db),
        _user: User = Depends(require_admin),
    ) -> ActivityPaymentDue:
        return ActivityPaymentService(db).validate(due_id)

Reserved for a treasurer role in the real project (a permission flag,
not just "any administrator") — this skeleton only implements
member/administrator, so `require_admin` stands in for it here; add a
real `require_treasurer_or_admin` dependency (same shape as
`require_admin` in api/deps.py) once that role exists.
"""
