from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ContentCreate(BaseModel):
    product_id: int | None = None
    platform: str | None = None
    title: str | None = None
    body: str = Field(min_length=1)
    media_url: str | None = None
    scheduled_at: datetime | None = None


class ContentResponse(BaseModel):
    id: int
    business_id: int
    product_id: int | None
    platform: str | None
    title: str | None
    body: str
    media_url: str | None
    status: str
    scheduled_at: datetime | None
    provider_post_id: str | None
    failure_reason: str | None

    model_config = ConfigDict(from_attributes=True)


class AIGenerateRequest(BaseModel):
    product_id: int
    platform: str
    language: str = "English"
    tone: str = "professional"
    goal: str = "sales"


class AIAdaptRequest(BaseModel):
    content_id: int
    platforms: list[str]
