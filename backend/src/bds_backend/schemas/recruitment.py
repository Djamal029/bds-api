"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class BecomePlayerRequest(BaseModel):
        code: str = Field(min_length=8, max_length=8)

    class RegistrationCodeRead(BaseModel):
        code: str
        expiration_date: datetime
        model_config = {"from_attributes": True}

    class RecruitPlayerCreate(BaseModel):
        team_id: uuid.UUID
        last_name: str = Field(min_length=1, max_length=100)
        first_name: str = Field(min_length=1, max_length=100)

Bounding `last_name`/`first_name` with `max_length` even though "a name
is too long" is a strange thing to reject: an unbounded string field on
a public-facing write endpoint is a standing invitation for someone to
send a megabyte of text, out of malice or by accident — cheap insurance
that costs the schema one keyword argument.
"""
