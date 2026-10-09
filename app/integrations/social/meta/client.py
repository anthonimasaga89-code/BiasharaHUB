import httpx
from app.core.config import settings


def graph_url(path: str) -> str:
    version = settings.META_GRAPH_VERSION.strip("/")
    return f"https://graph.facebook.com/{version}/{path.lstrip('/')}"


async def graph_get(path: str, access_token: str, params: dict | None = None) -> dict:
    query = dict(params or {})
    query["access_token"] = access_token
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(graph_url(path), params=query)
    response.raise_for_status()
    return response.json()


async def graph_post(path: str, access_token: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(graph_url(path), params={"access_token": access_token}, json=payload)
    response.raise_for_status()
    return response.json()
