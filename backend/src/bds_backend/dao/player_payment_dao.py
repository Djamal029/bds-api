"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class PlayerPaymentDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def get_or_create(
            self, player_id: uuid.UUID, type_: PaymentTypeEnum
        ) -> PlayerPayment:
            stmt = select(PlayerPayment).where(
                PlayerPayment.player_id == player_id, PlayerPayment.type == type_
            )
            payment = self._db.execute(stmt).scalar_one_or_none()
            if payment is None:
                payment = PlayerPayment(
                    player_id=player_id, type=type_, status=PaymentStatusEnum.PENDING
                )
                self._db.add(payment)
                self._db.flush()
            return payment

        def by_otp(
            self, player_id: uuid.UUID, otp: str, now: datetime
        ) -> list[PlayerPayment]:
            stmt = select(PlayerPayment).where(
                PlayerPayment.player_id == player_id,
                PlayerPayment.otp_code == otp,
                PlayerPayment.status == PaymentStatusEnum.PENDING,
                PlayerPayment.otp_expiration > now,
            )
            return list(self._db.execute(stmt).scalars().all())

Note `by_otp` checks `otp_expiration > now` in the query itself, not by
fetching the row and checking in Python — a code that's expired simply
isn't returned at all, which is both simpler and avoids a subtle bug
where "expired" and "wrong code" would otherwise need two different
code paths after the fetch.
"""
