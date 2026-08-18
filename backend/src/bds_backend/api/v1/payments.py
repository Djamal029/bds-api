"""STUB — not implemented. Copy the pattern from api/v1/auth.py.

    router = APIRouter(prefix="/payments", tags=["payments"])

    @router.post("/request", response_model=PaymentRequestResponse)
    def request_payment(
        data: PaymentRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> PaymentRequestResponse:
        player_id = _current_player_id(db, user)   # 404 if this account
                                                      # isn't linked to a player
        otp = PaymentService(db).request_payment(player_id, data.types)
        return PaymentRequestResponse(otp=otp, expires_in_seconds=300)

    @router.post("/validate-otp", response_model=list[PaymentRead])
    def validate_otp(
        data: OtpValidationRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ) -> list[PlayerPayment]:
        player_id = _current_player_id(db, user)
        try:
            return PaymentService(db).validate_otp(player_id, data.otp)
        except InvalidOtpError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

`_current_player_id` is a small route-local helper (not a service
method) that resolves the caller's own linked Player record and 404s
if there isn't one — every route in this file needs it, so it's worth
writing once at the top of the file rather than repeating the lookup
in every handler.
"""
