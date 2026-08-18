"""STUB — not implemented. Copy the pattern from schemas/auth.py.

    class PaymentRequest(BaseModel):
        types: list[PaymentTypeEnum] = Field(min_length=1)

    class PaymentRequestResponse(BaseModel):
        otp: str
        expires_in_seconds: int

    class OtpValidationRequest(BaseModel):
        otp: str = Field(min_length=6, max_length=6)

    class PaymentRead(BaseModel):
        type: PaymentTypeEnum
        status: PaymentStatusEnum
        validated_at: datetime | None
        model_config = {"from_attributes": True}

`OtpValidationRequest.otp`'s `min_length=6, max_length=6` (both set to
the same value) is a deliberate way to say "exactly 6 characters" with
Pydantic's `Field` — there's no dedicated `length=` parameter, so
pinning min and max to the same number is the idiomatic way to express
a fixed length.
"""
