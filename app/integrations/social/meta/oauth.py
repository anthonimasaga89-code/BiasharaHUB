from urllib.parse import urlencode
from app.core.config import settings


def build_meta_authorization_url(state: str, scopes: list[str]) -> str:
    if not settings.META_APP_ID:
        raise RuntimeError("META_APP_ID is not configured")
    params = {
        "client_id": settings.META_APP_ID,
        "redirect_uri": settings.META_REDIRECT_URI,
        "state": state,
        "scope": ",".join(scopes),
        "response_type": "code",
    }
    return "https://www.facebook.com/dialog/oauth?" + urlencode(params)


async def exchange_meta_code(code: str) -> dict:
    import httpx
    params = {
        "client_id": settings.META_APP_ID,
        "client_secret": settings.META_APP_SECRET,
        "redirect_uri": settings.META_REDIRECT_URI,
        "code": code,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://graph.facebook.com/oauth/access_token", params=params)
    response.raise_for_status()
    return response.json()
