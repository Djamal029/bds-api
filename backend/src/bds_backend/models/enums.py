"""STUB (partial) — `RoleEnum` is already implemented in `models/user.py`
(the one enum this skeleton's working feature actually needs). The real
project centralizes every enum in one `enums.py` instead of scattering
them across model files — once you implement more domains, move
`RoleEnum` here too and add the others alongside it:

    class FixtureStatusEnum(enum.StrEnum):
        SCHEDULED = "scheduled"
        IN_PROGRESS = "in_progress"
        FINISHED = "finished"
        CANCELLED = "cancelled"
        POSTPONED = "postponed"

    class OutcomeEnum(enum.StrEnum):
        HOME_WIN = "home_win"
        DRAW = "draw"
        AWAY_WIN = "away_win"

    class PracticeTypeEnum(enum.StrEnum):
        INDIVIDUAL = "individual"
        COLLECTIVE = "collective"

    class CategoryEnum(enum.StrEnum):
        FEMALE = "female"
        MALE = "male"
        MIXED = "mixed"

    class ActivityScopeEnum(enum.StrEnum):
        BDS_ONLY = "bds_only"
        ALL_SCHOOLS = "all_schools"
        RESTRICTED_LIST = "restricted_list"

    class PaymentTypeEnum(enum.StrEnum):
        JERSEY = "jersey"
        LICENSE = "license"

    class PaymentStatusEnum(enum.StrEnum):
        PENDING = "pending"
        VALIDATED = "validated"
        REJECTED = "rejected"

Each one is used as a column type via `mapped_column(SAEnum(TheEnum))` —
see `models/user.py`'s `role` column for the exact pattern.
"""
