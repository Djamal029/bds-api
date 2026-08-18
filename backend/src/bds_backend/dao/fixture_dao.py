"""STUB — not implemented. Copy the pattern from dao/user_dao.py.

    class FixtureDAO:
        def __init__(self, db: Session) -> None:
            self._db = db

        def list_upcoming(self, limit: int = 20) -> list[Fixture]:
            stmt = (
                select(Fixture)
                .where(Fixture.status == FixtureStatusEnum.SCHEDULED)
                .order_by(Fixture.date_time)
                .limit(limit)
            )
            return list(self._db.execute(stmt).scalars().all())

        def upsert_result(
            self, fixture_id: uuid.UUID, home_score: int, away_score: int
        ) -> FixtureResult:
            existing = self._db.execute(
                select(FixtureResult).where(FixtureResult.fixture_id == fixture_id)
            ).scalar_one_or_none()
            outcome = (
                OutcomeEnum.HOME_WIN if home_score > away_score
                else OutcomeEnum.AWAY_WIN if home_score < away_score
                else OutcomeEnum.DRAW
            )
            if existing is None:
                result = FixtureResult(
                    fixture_id=fixture_id, home_score=home_score,
                    away_score=away_score, outcome=outcome,
                )
                self._db.add(result)
            else:
                existing.home_score = home_score
                existing.away_score = away_score
                existing.outcome = outcome
                result = existing
            self._db.flush()
            return result

A list query that needs both teams' names (for display) should join
`Team` twice, aliased once per side (`aliased(Team)` for home and away)
— joining the same table twice under one alias each is the standard
SQLAlchemy pattern for a self-referencing-style join like a fixture's
home/away teams, avoid the temptation to fetch each team's name with a
separate query per fixture (an N+1 query bug).
"""
