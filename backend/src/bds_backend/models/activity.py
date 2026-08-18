"""STUB — not implemented. Copy the pattern from models/user.py.

An event beyond a regular fixture: a tournament, an outing, a social —
anything a member registers for, optionally paying installments and/or
a deposit (see models/activity_payment.py, models/activity_registration.py,
both stubs).

    class Activity(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "activities"

        name: Mapped[str] = mapped_column(String(150))
        description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
        date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
        location: Mapped[str | None] = mapped_column(String(255), nullable=True)
        creator_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
        scope: Mapped[ActivityScopeEnum] = mapped_column(SAEnum(ActivityScopeEnum))
        image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
        practice_type: Mapped[PracticeTypeEnum] = mapped_column(SAEnum(PracticeTypeEnum))
        max_spots: Mapped[int | None] = mapped_column(Integer, nullable=True)
        # Derived/display total, not the source of truth once installments
        # exist — see activity_payment.py's ActivityInstallment for why the
        # real total is the SUM of installment amounts, this field is a
        # convenience for free/simple activities with no installments.
        amount: Mapped[str | None] = mapped_column(String(20), nullable=True)

`max_spots: None` means unlimited — see services/activity_service.py's
(hypothetical, once you build it) registration logic for how that
distinction has to be checked explicitly, `if max_spots is not None`,
never treated as "0 means unlimited" or similar.
"""
