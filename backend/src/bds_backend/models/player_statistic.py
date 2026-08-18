"""STUB — not implemented. Copy the pattern from models/user.py.

One player's statistics for one fixture (composite of Player x Fixture).

    class PlayerStatistic(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "player_statistics"

        player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"))
        fixture_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fixtures.id"))
        goals: Mapped[int] = mapped_column(Integer, default=0)
        assists: Mapped[int] = mapped_column(Integer, default=0)
        minutes_played: Mapped[int] = mapped_column(Integer, default=0)

Add a unique constraint on `(player_id, fixture_id)` — one statistics
row per player per fixture, not several — via `UniqueConstraint` in a
`__table_args__` tuple (see SQLAlchemy docs for the exact syntax; it's
the multi-column equivalent of a single `unique=True` on one column).
"""
