"""STUB — not implemented. Copy the pattern from services/auth_service.py.

    class PaymentService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = PlayerPaymentDAO(db)
            self._notifications = NotificationService(db)

        def request_payment(
            self, player_id: uuid.UUID, types: list[PaymentTypeEnum]
        ) -> str:
            otp = f"{secrets.randbelow(1_000_000):06d}"
            for type_ in types:
                payment = self._dao.get_or_create(player_id, type_)
                payment.otp_code = otp
                payment.otp_expiration = datetime.now(UTC) + timedelta(minutes=5)
            self._notifications.notify(..., "Payment code requested", ...)
            self._db.commit()   # one commit for every payment row touched
                                 # in the loop above, plus the notification
            return otp

        def validate_otp(self, player_id: uuid.UUID, otp: str) -> list[PlayerPayment]:
            now = datetime.now(UTC)
            payments = self._dao.by_otp(player_id, otp, now)
            if not payments:
                raise InvalidOtpError(...)
            for payment in payments:
                payment.status = PaymentStatusEnum.VALIDATED
                payment.otp_code = None
            self._db.commit()
            return payments

Note `request_payment` commits ALL the loop's writes together in one
commit, not once per payment type inside the loop — they're one logical
operation ("a code was requested for these payment types"), so they
succeed or fail together.
"""
