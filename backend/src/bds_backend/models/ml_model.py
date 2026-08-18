"""STUB — not implemented, and well out of scope for a first
contribution. Metadata about a trained prediction model (see
models/prediction.py), not the model itself — actual model training is
explicitly out of scope for this codebase (a simple deterministic
algorithm, not a real trained model, is the expected implementation
whenever this is built).

    class MLModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "ml_models"

        name: Mapped[str] = mapped_column(String(100))
        version: Mapped[str] = mapped_column(String(20))
        is_active: Mapped[bool] = mapped_column(Boolean, default=False)
"""
