"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class AuditLogEntryRead(BaseModel):
        id: uuid.UUID
        user_email: str       # joined in, not the raw user_id — see
                                # dao/audit_log_entry_dao.py's stub for
                                # the join this comes from
        action: str
        entity: str
        entity_id: uuid.UUID | None
        details: str | None
        created_at: datetime
        model_config = {"from_attributes": True}

Named `journal.py` (not `audit_log.py`) in the real project this
skeleton mirrors — schema file names don't always match their model's
file name 1:1 when the response shape crosses domains (this one reads
from `AuditLogEntry` but is really about "the journal an admin views",
which is the more useful name for the API consumer).
"""
