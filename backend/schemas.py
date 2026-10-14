from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PaymentRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    student_reference: str = Field(min_length=2, max_length=80, pattern=r"^[\w .:/-]+$")
    recipient_name: str = Field(min_length=2, max_length=120)
    recipient_reference: str = Field(min_length=3, max_length=80, pattern=r"^[\w .:/-]+$")
    amount: float = Field(gt=0, le=100000, allow_inf_nan=False)
    currency: Literal["AUD", "USD", "BDT", "SAR"] = "AUD"
    purpose: str = Field(default="tuition", min_length=3, max_length=200)
