"""STUB — not implemented. Copy the pattern from models/user.py.

A single-use code an administrator generates for a recruited Player, so
the real person can later link their own Member account to that
pre-created player record without an admin doing it manually.

    class RegistrationCode(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "registration_codes"

        code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
        player_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("players.id"), unique=True
        )
        expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
        used: Mapped[bool] = mapped_column(Boolean, default=False)
        used_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True
        )

`player_id` is `unique=True` too: at most one active code per player,
consistent with "a player is either already linked to an account, has
an outstanding code, or has neither" — never two live codes for the
same not-yet-claimed player.
"""
