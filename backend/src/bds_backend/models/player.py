"""STUB — not implemented. Copy the pattern from models/user.py.

A player record, distinct from a User account: an administrator
pre-creates a Player (attached to a Team) before the actual person has
an account, then a Member later links their own account to it (see
models/registration_code.py for how — out of scope to fully re-derive
here, ask about the recruitment flow once you're building this).

    class Player(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "players"

        last_name: Mapped[str] = mapped_column(String(100))
        first_name: Mapped[str] = mapped_column(String(100))
        nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
        position: Mapped[str | None] = mapped_column(String(50), nullable=True)
        birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
        team_id: Mapped[uuid.UUID | None] = mapped_column(
            ForeignKey("teams.id"), nullable=True
        )
        # Set once a Member account claims this player record. Nullable AND
        # unique: nullable because a freshly created Player has no linked
        # account yet, unique because one account can only ever be linked
        # to one player.
        user_id: Mapped[uuid.UUID | None] = mapped_column(
            ForeignKey("users.id"), unique=True, nullable=True
        )
"""
