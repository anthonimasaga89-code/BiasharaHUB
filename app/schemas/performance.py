from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PerformanceCreate(BaseModel):
    content_id: int
    platform: str
    metric_name: str
    metric_value: float = Field(ge=0)


class PerformanceResponse(BaseModel):
    id: int
    content_id: int
    platform: str
    metric_name: str
    metric_value: float
    captured_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionRequest(BaseModel):
    platform: str
    content_length: float = 0
    hashtag_count: float = 0
    hour: float = 12
    day_of_week: float = 0
    historical_engagement: float = 0


class PredictionResponse(BaseModel):
    predicted_performance: float
    model: str
    trained: bool
