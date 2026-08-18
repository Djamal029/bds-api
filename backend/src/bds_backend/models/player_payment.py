"""STUB — not implemented. Copy the pattern from models/user.py.

A player's jersey/license payment, tracked through an OTP-code flow
(the player requests a code, a treasurer or the player themselves
enters it to mark the payment validated — real money never moves inside
the app, this only tracks status).

    class PlayerPayment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "player_payments"

        player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"))
        type: Mapped[PaymentTypeEnum] = mapped_column(SAEnum(PaymentTypeEnum))
        status: Mapped[PaymentStatusEnum] = mapped_column(
            SAEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING
        )
        otp_code: Mapped[str | None] = mapped_column(String(6), nullable=True)
        otp_expiration: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True
        )
        validated_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True
        )
        rejection_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)

One row per `(player_id, type)` in practice — a service method should
fetch-or-create rather than blindly inserting, so requesting a code
twice for the same payment type reuses the same row (see
services/team_service.py's stub for the general "service owns the
commit, DAO only flushes" reminder, which applies here too).
"""
