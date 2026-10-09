from datetime import datetime, timedelta, timezone
import secrets
from urllib.parse import urlencode
import jwt
import httpx

from app.core.config import settings


def create_state(user_id: int, business_id: int) -> str:
    payload = {
        "user_id": user_id,
        "business_id": business_id,
        "nonce": secrets.token_urlsafe(16),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_state(state: str) -> dict:
    return jwt.decode(state, settings.SECRET_KEY, algorithms=["HS256"])


def build_authorization_url(state: str) -> str:
    if not settings.LINKEDIN_CLIENT_ID:
        raise RuntimeError("LINKEDIN_CLIENT_ID is not configured")
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "state": state,
        "scope": settings.LINKEDIN_SCOPES,
    }
    return "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)


async def exchange_code(code: str) -> dict:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post("https://www.linkedin.com/oauth/v2/accessToken", data=data)
    response.raise_for_status()
    return response.json()
