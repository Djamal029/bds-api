"""STUB — not implemented. Copy the pattern from schemas/auth.py.

You'll want at minimum:

    class TeamCreate(BaseModel):
        name: str = Field(min_length=1, max_length=150)
        sport_id: uuid.UUID
        season: str

    class TeamRead(BaseModel):
        id: uuid.UUID
        name: str
        sport: str          # the sport's NAME, not just its id — joined
                             # in at the DAO level so the frontend doesn't
                             # need a second request just to show it
        season: str
        model_config = {"from_attributes": True}

Note `TeamRead.sport` above: a response schema is free to shape data
differently from the underlying table — it exists to serve the API
consumer, not to mirror the database 1:1. See schemas/auth.py's WHY
note on request vs response schemas for the same idea applied to hiding
`password_hash`.
"""
