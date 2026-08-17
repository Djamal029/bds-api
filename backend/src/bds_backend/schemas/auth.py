"""Request and response shapes for authentication.

WORKED EXAMPLE — fully implemented, read this one closely.

WHY every route accepts a Pydantic schema, never a raw dict or an ORM
model, as its request body: a schema is an explicit allow-list of
fields. `MemberRegistration` below has no `role` field, so there is no
way for a client to register themselves as an administrator by adding
an extra `"role": "administrator"` key to the JSON body — FastAPI
rejects unknown fields by default (or silently drops them, depending on
config; either way, `role` is never set from client input, only ever
by the service layer itself, hardcoded to `RoleEnum.MEMBER`, see
services/auth_service.py).

WHY a separate `UserRead` (response) vs `MemberRegistration` (request)
even though they overlap: `UserRead` intentionally excludes
`password_hash` — returning an ORM `User` object directly through a
schema that doesn't ask for that field means it can never accidentally
leak into an API response, no matter what the route handler does with
the object internally.

WHY `model_config = {"from_attributes": True}` on `UserRead`: this lets
Pydantic build the response directly from an ORM object's attributes
(`user.email`, `user.role`, ...) instead of requiring the route to
manually construct a dict first.
"""

import uuid

from pydantic import BaseModel, EmailStr, Field

from bds_backend.models.user import RoleEnum


class MemberRegistration(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdate(BaseModel):
    """Every field optional: a PATCH only ever changes what's provided,
    everything else on the account is left untouched. See
    services/auth_service.update_profile() for how `None` vs an actual
    value is distinguished (`None` means "don't touch this field", it does
    NOT mean "clear this field to empty" — a real product might need a
    separate sentinel for that distinction, out of scope here)."""

    username: str | None = Field(default=None, min_length=3, max_length=50)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: str
    username: str | None
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}
