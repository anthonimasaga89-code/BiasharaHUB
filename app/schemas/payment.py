from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    order_id: int
    provider: str
    amount: Decimal = Field(gt=0)
    phone: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    provider: str
    reference: str
    amount: Decimal
    currency: str
    status: str

    model_config = ConfigDict(from_attributes=True)
