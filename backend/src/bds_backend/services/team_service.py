"""STUB — not implemented. Copy the pattern from services/auth_service.py.

You'll want at minimum:

    class TeamService:
        def __init__(self, db: Session) -> None:
            self._db = db
            self._dao = TeamDAO(db)

        def create_team(self, data: TeamCreate) -> Team:
            team = Team(name=data.name, sport_id=data.sport_id, season=data.season)
            created = self._dao.create(team)
            self._db.commit()   # ONE commit, after every write this
                                 # operation needed — see auth_service.py's
                                 # module docstring for the full reasoning
            return created

The one rule to keep in mind, restated once more because it's the whole
point of this skeleton: this service owns `self._db.commit()`. The DAO
it calls only ever flushes. If a service method calls more than one DAO
write, all of them happen before the single commit at the end (or,
if some should be independently durable regardless of what happens
next — e.g. a bulk-import processing many independent rows where one
bad row shouldn't undo the good ones — commit after each independent
unit instead of once at the very end; that's a deliberate exception to
"one commit per method", not a contradiction of the rule, since each
row IS its own complete unit of work in that case).
"""
