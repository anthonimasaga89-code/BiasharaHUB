import httpx
from urllib.parse import urlencode
from app.core.config import settings


def build_authorization_url(state: str) -> str:
    params = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "response_type": "code",
        "scope": settings.TIKTOK_SCOPES,
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
        "state": state,
    }
    return "https://www.tiktok.com/v2/auth/authorize/?" + urlencode(params)


async def exchange_code(code: str) -> dict:
    data = {
        "client_key": settings.TIKTOK_CLIENT_KEY,
        "client_secret": settings.TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.TIKTOK_REDIRECT_URI,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post("https://open.tiktokapis.com/v2/oauth/token/", data=data)
    response.raise_for_status()
    return response.json()


async def get_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://open.tiktokapis.com/v2/user/info/",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"fields": "open_id,display_name,avatar_url"},
        )
    response.raise_for_status()
    return response.json()


async def query_creator_info(access_token: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        )
    response.raise_for_status()
    return response.json()
