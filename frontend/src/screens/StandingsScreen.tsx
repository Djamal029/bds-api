/**
 * STUB — not implemented, and needs a new backend route first: a league
 * table (played/won/drawn/lost/points per team for a sport+season,
 * computed from every finished Fixture's FixtureResult). Out of scope to
 * fully re-derive the aggregation logic here — once fixtures work
 * end to end (see models/fixture.py's stub), this becomes a
 * `FixtureDAO.standings(sport_id, season)` method building the table in
 * Python from the finished fixtures, not a single SQL aggregate query
 * (home/away scoring makes a pure-SQL version awkward — computing it
 * in Python after one query per fixture is simpler and clear enough at
 * this scale).
 */

export {};
