"""STUB — not implemented. Copy the pattern from models/user.py.

A scheduled or completed match: links a Sport and two Teams (see
models/sport.py, models/team.py, both stubs).

    class Fixture(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "fixtures"

        sport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sports.id"))
        home_team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
        away_team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
        date_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
        location: Mapped[str | None] = mapped_column(String(255), nullable=True)
        status: Mapped[FixtureStatusEnum] = mapped_column(SAEnum(FixtureStatusEnum))

Needs `FixtureStatusEnum` from models/enums.py (also a stub) implemented
first. Its final score lives in a separate table, see
models/fixture_result.py — a Fixture can exist (scheduled) with no
result yet, which is exactly why score isn't just two nullable columns
on this table.
"""
