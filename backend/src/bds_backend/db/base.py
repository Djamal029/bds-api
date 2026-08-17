"""The SQLAlchemy declarative base every model inherits from.

WORKED EXAMPLE — fully implemented (there is genuinely nothing more to
it than this).

WHY this is its own file instead of living in db/session.py or a model
file: every model module needs to import `Base` to define a table, and
`db/session.py` also needs to import every model (indirectly, via
`bds_backend.models`) to call `Base.metadata.create_all(...)`. Putting
`Base` in a third, dependency-free file avoids a circular import between
"the models" and "the thing that creates their tables".
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
