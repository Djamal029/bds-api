"""STUB — not implemented, and out of scope for a first contribution.
A predicted outcome for an upcoming Fixture, produced by whatever
implements models/ml_model.py.

    class Prediction(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "predictions"

        fixture_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fixtures.id"))
        model_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("ml_models.id"))
        predicted_outcome: Mapped[OutcomeEnum] = mapped_column(SAEnum(OutcomeEnum))
        confidence: Mapped[str | None] = mapped_column(String(10), nullable=True)
"""
