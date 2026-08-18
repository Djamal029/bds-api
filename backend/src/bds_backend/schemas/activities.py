"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class ActivityCreate(BaseModel):
        name: str = Field(min_length=1, max_length=150)
        description: str | None = Field(default=None, max_length=2000)
        date_time: datetime
        location: str | None = Field(default=None, max_length=255)
        max_spots: int | None = Field(default=None, ge=1)

    class ActivityRead(BaseModel):
        id: uuid.UUID
        name: str
        date_time: datetime
        location: str | None
        spots_remaining: int | None   # derived, not a stored column — see
                                        # dao/activity_registration_dao.py's
                                        # stub for the count query behind it
        is_registered: bool           # derived per-caller: True only if
                                        # the requesting user is registered,
                                        # never a stored column either
        model_config = {"from_attributes": True}

`ActivityRead`'s `spots_remaining`/`is_registered` can't come from
`model_config = {"from_attributes": True}` alone reading straight off
the ORM object, since neither is a real column — the SERVICE has to
compute them (a registration count, a per-user membership check) and
build the response explicitly, field by field, rather than validating
directly from the ORM instance for this one response shape.
"""
