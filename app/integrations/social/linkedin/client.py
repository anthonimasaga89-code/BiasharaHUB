from datetime import datetime, timedelta
import httpx

from app.core.config import settings


async def get_member_profile(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    response.raise_for_status()
    return response.json()


async def create_text_post(access_token: str, author_urn: str, commentary: str) -> str:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Linkedin-Version": settings.LINKEDIN_API_VERSION if hasattr(settings, "LINKEDIN_API_VERSION") else "202604",
    }
    payload = {
        "author": author_urn,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post("https://api.linkedin.com/rest/posts", headers=headers, json=payload)
    response.raise_for_status()
    return response.headers.get("x-restli-id", "")
