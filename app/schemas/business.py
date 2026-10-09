from pydantic import BaseModel, ConfigDict, Field


class BusinessCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    phone: str | None = None
    location: str | None = None


class BusinessUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    phone: str | None = None
    location: str | None = None
    status: str | None = None


class BusinessResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    description: str | None
    phone: str | None
    location: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)
