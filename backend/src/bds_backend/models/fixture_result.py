"""STUB — not implemented. Copy the pattern from models/user.py.

The final score of a Fixture, once it has one. A separate table from
`Fixture` (composition: this row does not exist without its Fixture) so
a scheduled-but-not-yet-played fixture has no score row at all, instead
of two nullable `home_score`/`away_score` columns on Fixture itself that
would be meaningless (not just empty) before the match happens.

    class FixtureResult(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "fixture_results"

        fixture_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("fixtures.id"), unique=True
        )
        home_score: Mapped[int] = mapped_column(Integer)
        away_score: Mapped[int] = mapped_column(Integer)
        outcome: Mapped[OutcomeEnum] = mapped_column(SAEnum(OutcomeEnum))

`unique=True` on `fixture_id` is what enforces "at most one result per
fixture" at the database level, not just in application code.
"""
