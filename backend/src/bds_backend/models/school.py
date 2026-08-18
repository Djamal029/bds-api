"""STUB — not implemented. Copy the pattern from models/user.py.

Reference list of schools other than our own (used as an Activity's
scope target and, once implemented, to mark a Team as belonging to
another school rather than ours).

    class School(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "schools"

        name: Mapped[str] = mapped_column(String(150), unique=True)
        city: Mapped[str | None] = mapped_column(String(100), nullable=True)
"""
