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

## Data model

`diagramme_classes_bds_api.html` has the full class diagram — not just
what's implemented today, but the target model every roadmap phase
below builds toward, color-coded by which phase introduces each class,
plus a relationships table (every foreign key, its multiplicity, and
which two classes it connects). Read it alongside the roadmap; the two
are meant to update together.

## Build roadmap: from auth-only to a full BDS MVP

This is the team's plan for building the rest of the platform in this
skeleton, from where it stands today (one working domain: auth) toward
feature parity with the real BDS app. It follows the same rule as the
real project's own roadmap: **one step, one collaborator, smallest
first, nothing marked done until its MVP clears the full gate** (ruff,
mypy, pytest, `tsc --noEmit`, a manual pass through the golden path).

**Target: a usable core app by 15 October 2026.** That's about 8-9
weeks from today (18 August 2026). This plan assumes 2-3 collaborators
working in parallel on independent domains (a domain is "independent"
if it doesn't share a model with a domain someone else is mid-step on)
— adjust the pacing below to the team's actual size; the *order* and
*MVP scope* of each step matter more than the exact dates. If the team
is smaller or slower than assumed, Phase D is the part to slip past the
deadline first, not Phases A-C.

Each domain already exists as stub files in this skeleton (see the
table in `CONTRIBUTING.md`) with a docstring pointing at the worked
auth example. Once a full BDS checkout is available for reference, its
already-built version of each domain is a second reference — read the
stub's own docstring first, since it's written for this skeleton's
narrower scope, not the full product's.

### Phase A — Foundations (target: 29 Aug 2026)

Small, mostly independent reference-data domains. Good first steps for
new collaborators since each is a complete, low-risk pass through every
layer.

| # | Step | MVP | Size |
|---|---|---|---|
| A1 | Sports | Admin creates a sport (name, description); anyone lists sports. No edit/delete yet. | Smallest |
| A2 | Schools | Admin creates a school (name); anyone lists schools. Needed later by activity scope and cross-school rosters. | Smallest |
| A3 | Security baseline | Per-IP rate limiting on `/auth/register`, `/auth/login`, `/auth/refresh`; per-account lockout after repeated failed logins. Touches only `core/` and `services/auth_service.py` — do this before other domains build on auth, not after. | Small |
| A4 | Teams | Admin creates a team (name, sport, season); anyone lists teams for a sport/season. Depends on A1. | Small |

### Phase B — Core sports domain (target: 19 Sep 2026)

| # | Step | MVP | Size |
|---|---|---|---|
| B1 | Players & rosters | Admin adds a player to a team (first/last name, position); anyone views a team's roster. Depends on A4. | Small-medium |
| B2 | Recruitment codes | Admin generates a one-time registration code for a player; a member redeems it to link their account, or self-registers as a supporter with no code. Depends on B1. | Small-medium |
| B3 | Fixtures & results | Admin creates a fixture (two teams, date, location); a reporter starts it, enters a score, closes it (outcome computed automatically). Depends on A4. | Medium |
| B4 | Standings | League table computed from closed fixtures for a sport/season, ranked by points. Depends on B3. | Small |

### Phase C — Activities and payments (target: 3 Oct 2026)

The revenue-critical domain — money never moves in-app, but every
payment's state (pending/validated/rejected/refund-due) must be exact.

| # | Step | MVP | Size |
|---|---|---|---|
| C1 | Activities | Admin creates an activity (name, date, description, optional max spots); any account browses and registers. No payment yet. | Medium |
| C2 | Activity payments | Registering for a paid activity creates pending dues (installments + optional deposit); treasurer validates or rejects each, with a reason if rejected. Depends on C1. | Medium-large |
| C3 | Player payments | A member requests a player payment (jersey/license), confirms via OTP; treasurer reviews it the same way as C2. | Medium |
| C4 | Registration/refund deadlines | Optional deadlines on an activity: after the registration deadline, registering is refused; cancelling before the refund deadline flags a validated due as refundable instead of just disappearing. Depends on C1-C2. | Small |

### Phase D — Platform features (target: 15 Oct 2026)

Can run on a second track in parallel with Phase C, since it touches
different models.

| # | Step | MVP | Size |
|---|---|---|---|
| D1 | Notifications | A notification bell with unread count; the system auto-creates one when a payment becomes due, is validated, or is rejected (reason included). | Small-medium |
| D2 | Administration | Admin lists every account, searches by username, grants/revokes role flags, activates/deactivates accounts; every write is recorded to an audit log. | Medium |
| D3 | Match predictions | Any account picks a scheduled fixture's outcome (and optionally its exact score); scored automatically when the fixture closes (3 points exact score, 1 correct outcome, 0 wrong); a leaderboard, global and per-sport. Depends on B3. | Medium |

### Phase E — Stretch goals (beyond 15 Oct 2026 unless ahead of schedule)

Everything here is genuinely optional for the mid-October target. Pick
these up only once Phases A-D are done and gated.

| # | Step | MVP | Size |
|---|---|---|---|
| E1 | Tablet-optimized reporter layout | Two-column layout with larger touch targets on the fixture-scoring screen above a tablet width breakpoint. Frontend-only. | Smallest |
| E2 | Jersey number and name reservation | Jersey number + name-on-jersey set when adding a player to a roster, unique per team/season. | Small |
| E3 | Automatic playing-time tracking | Substitution events (player out, player in, minute) recorded per fixture; `minutes_played` computed from them instead of typed by hand. | Medium |
| E4 | Excel import of historical results | Admin uploads a single `.xlsx` of fixtures for one sport/season; validated row-by-row before anything is written. | Largest |

### How to pick up a step

1. Read the stub files for that domain (docstrings list the minimum
   fields and point at the worked example to copy).
2. Follow the 9-step checklist in `CONTRIBUTING.md`'s "Adding a whole
   new feature" section, layer by layer.
3. Write the test file before calling it done, not after — a step
   without a passing test for its golden path isn't done, no matter
   how the screen looks.
4. Run the full gate. Open a PR. Update this table's status in the
   same PR.
