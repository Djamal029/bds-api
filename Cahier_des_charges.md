# Cahier des charges (skeleton scope)

This is the product context for the architecture skeleton in this
repository, not the full specification for the real BDS platform. It
exists so the architecture choices in `CONTRIBUTING.md` make sense in
context, even though most of the real product's features are stubs
here.

## What BDS is

Bureau des Sports (BDS) is a school sports club. The real platform is
a mobile app plus a backend API covering five domains: sport results
and fixtures, paid and free activities, player recruitment, user
administration, and notifications.

This skeleton implements exactly one of those domains, fully: account
registration and login. Every other domain (teams, fixtures,
activities, payments, notifications) is present only as an empty
model/schema/DAO/service/route file with a docstring explaining what it
needs, pointing back at the one implemented domain as the pattern to
copy.

## Why this scope

A new contributor learns the architecture faster from one complete,
working, testable feature than from a large codebase where the pattern
is scattered across hundreds of files. Authentication was chosen
because every other feature depends on it (a route needs to know who
is calling it before anything else matters), so understanding it first
is not wasted effort.

## Roles

The real platform has six roles: member, player, treasurer, score
reporter, fixture manager, administrator, and super administrator (see
`CONTRIBUTING.md`'s worked-example section for where role checks live).
This skeleton implements two: `member` and `administrator`, enough to
demonstrate the pattern (`api/deps.py`'s `require_role(...)`) without
building out every permission a real deployment would need.

## Database

SQLite by default, portable to MySQL or Postgres without touching a
query, because every database access goes through SQLAlchemy's ORM,
never raw engine-specific SQL. See `CONTRIBUTING.md` for the exact
setup and the one caveat (SQLite cannot run this project's — hypothetical,
once it has one — MySQL-only Alembic migration chain).

## Where to go from here

Implement one more domain end to end (teams is the natural next choice,
since fixtures and rosters depend on it) following the six-step list at
the bottom of `models/sport.py` and `models/team.py`. Once one more
domain works end to end, the pattern should be clear enough to build
the rest without needing further worked examples.
