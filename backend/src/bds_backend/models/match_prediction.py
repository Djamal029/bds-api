"""STUB — not implemented. Copy the pattern from models/user.py.

A member's pick for how a Fixture will end, submitted before it starts,
and scored once it closes — the "pronostics" game (see
`Cahier_des_charges.md`'s roadmap, step D3). Deliberately unrelated to
models/prediction.py and models/ml_model.py, which are a different,
out-of-scope concept (a machine-learning model's own probability
estimate for a fixture) — this table is scored against the real result,
never against a model's output, and has no dependency on either stub.

    class MatchPrediction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "match_predictions"
        __table_args__ = (
            UniqueConstraint("fixture_id", "user_id", name="uq_match_prediction_user"),
        )

        fixture_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fixtures.id"))
        user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
        predicted_outcome: Mapped[OutcomeEnum] = mapped_column(SAEnum(OutcomeEnum))
        predicted_home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
        predicted_away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
        points_earned: Mapped[int | None] = mapped_column(Integer, nullable=True)

A pick always has an outcome; an exact score is optional on top of it,
and if given, both halves must be set together and must agree with the
picked outcome (validate this in schemas/predictions.py, not here — see
schemas/auth.py for where request-level cross-field validation belongs).
`points_earned` stays null until the fixture has a result: 3 points for
an exact score match, 1 for a correct outcome alone (or a wrong score),
0 for a wrong outcome. It is set once, from
`services/fixture_service.py`'s (stub) score-closing method, and never
edited afterward — a settled pick is a historical record.
"""
