"""STUB — not implemented. Copy the pattern from models/user.py.

A `Team` belongs to one `Sport` (models/sport.py, also a stub) and one
season (a plain string like "2026-2027" works fine, no need for a
separate Season table unless you need to attach data to a season
itself). A Team has many Players.

To implement, you need at minimum:

    class Team(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "teams"

        name: Mapped[str] = mapped_column(String(150))
        sport_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sports.id"))
        season: Mapped[str] = mapped_column(String(20))

For the foreign key pattern (`sport_id: Mapped[uuid.UUID] = mapped_column(
ForeignKey("sports.id"))`), see how `models/user.py`'s `Member`/
`Administrator` classes link back to `users.id` — same idea, a plain
column holding another table's primary key, not a full relationship
object (this codebase's DAOs build explicit `select(...).join(...)`
queries rather than relying on lazy-loaded ORM relationships, precisely
to keep query costs visible and avoid N+1 queries — see any DAO in the
real project's `dao/` folder for that pattern once you have access to
it, or dao/user_dao.py here for the general DAO shape).

Once implemented, follow the same 6 steps listed at the bottom of
models/sport.py (schema, DAO, service, routes, test).
"""
