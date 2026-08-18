"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class FixtureRead(BaseModel):
        id: uuid.UUID
        sport: str            # the sport's name, joined in at the DAO
                                # level — see schemas/teams.py's stub for
                                # the same "shape the response, don't
                                # mirror the table" idea
        home_team: str
        away_team: str
        date_time: datetime
        status: FixtureStatusEnum
        home_score: int | None = None
        away_score: int | None = None
        model_config = {"from_attributes": True}

    class FixtureScoreUpdate(BaseModel):
        home_score: int = Field(ge=0)
        away_score: int = Field(ge=0)
        close: bool = False

`Field(ge=0)` on both scores: a negative score is never legitimate, so
reject it at the schema layer (a 422 before the request even reaches a
service) rather than trusting the caller or checking it deeper in the
stack.
"""
