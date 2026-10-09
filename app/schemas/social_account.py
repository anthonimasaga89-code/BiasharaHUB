from pydantic import BaseModel, ConfigDict


class SocialAccountResponse(BaseModel):
    id: int
    business_id: int
    platform: str
    account_name: str
    account_id: str
    is_connected: bool

    model_config = ConfigDict(from_attributes=True)


class SocialConnectRequest(BaseModel):
    platform: str


class SocialManualConnectRequest(BaseModel):
    platform: str
    account_name: str
    account_id: str
    access_token: str
    refresh_token: str | None = None
