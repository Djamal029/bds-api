"""STUB — not implemented, and out of scope until a bulk-import feature
(e.g. importing historical fixture results from a PDF/Excel file, see
services/recruitment_service.py's real-project equivalent for the
"bulk import, per-row independent commit" pattern once it applies here
too) is actually being built.

    class ImportHistory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "import_history"

        uploaded_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
        filename: Mapped[str] = mapped_column(String(255))
        status: Mapped[ImportStatusEnum] = mapped_column(SAEnum(ImportStatusEnum))
        summary: Mapped[str | None] = mapped_column(String(2000), nullable=True)
"""
