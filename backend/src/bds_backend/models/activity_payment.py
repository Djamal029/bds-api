"""STUB — not implemented. Copy the pattern from models/user.py.

Three related tables for an activity's payment structure:

    class ActivityInstallment(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "activity_installments"
        activity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("activities.id"))
        label: Mapped[str] = mapped_column(String(100))     # e.g. "Jersey"
        amount: Mapped[str] = mapped_column(String(20))     # store money as a
                                                              # string or Numeric,
                                                              # never float
        due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    class ActivityDeposit(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "activity_deposits"
        activity_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("activities.id"), unique=True   # at most one deposit
        )
        label: Mapped[str] = mapped_column(String(100))
        amount: Mapped[str] = mapped_column(String(20))
        requires_check: Mapped[bool] = mapped_column(Boolean, default=False)

    class ActivityPaymentDue(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "activity_payment_dues"
        registration_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("activity_registrations.id")
        )
        installment_id: Mapped[uuid.UUID | None] = mapped_column(
            ForeignKey("activity_installments.id"), nullable=True
        )
        deposit_id: Mapped[uuid.UUID | None] = mapped_column(
            ForeignKey("activity_deposits.id"), nullable=True
        )
        status: Mapped[PaymentStatusEnum] = mapped_column(
            SAEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING
        )
        rejection_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
        validated_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True
        )
        paid_by_check: Mapped[bool] = mapped_column(Boolean, default=False)

One `ActivityPaymentDue` row is created per installment (plus one more
for the deposit, if the activity has one) the moment a member
registers — see models/activity_registration.py's stub. Exactly one of
`installment_id`/`deposit_id` is set per row, never both, never
neither: this is the kind of constraint a plain nullable-FK pair cannot
enforce at the database level (a `CheckConstraint` can, if you want to
go further than this skeleton does).
"""
