"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class AccountStatusUpdate(BaseModel):
        is_active: bool

    class RoleUpdate(BaseModel):
        role: RoleEnum

Deliberately tiny, one field each: a PATCH endpoint's request schema
should accept exactly what it changes and nothing else — resist the
urge to reuse a bigger "UserUpdate" schema with lots of optional fields
for two single-purpose endpoints, that would let a client set fields
this specific route was never meant to touch (see schemas/auth.py's
module docstring on why a schema is an allow-list, not just a
validation convenience).
"""
