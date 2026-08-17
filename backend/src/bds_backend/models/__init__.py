"""Re-exports every model so `Base.metadata` knows about every table.

WHY this matters: `Base.metadata.create_all(engine)` (used by
scripts/bootstrap_sqlite_dev.py and tests/conftest.py) only creates
tables for models that have actually been imported somewhere by the
time it runs — SQLAlchemy discovers tables by import side-effect, not
by scanning the filesystem. Importing every model here, once, and
importing `bds_backend.models` (this package) wherever the full schema
needs to exist, is what guarantees nothing gets silently left out.

When you implement models/team.py or models/sport.py, add them here too.
"""

from bds_backend.models.user import Administrator, Member, RoleEnum, User

__all__ = ["Administrator", "Member", "RoleEnum", "User"]
