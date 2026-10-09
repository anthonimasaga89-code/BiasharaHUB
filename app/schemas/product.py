from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    location: str | None = None
    contact: str | None = None
    delivery_information: str | None = None
    image_url: str | None = None
    video_url: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    location: str | None = None
    contact: str | None = None
    delivery_information: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    status: str | None = None


class ProductResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    location: str | None
    contact: str | None
    delivery_information: str | None
    image_url: str | None
    video_url: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
