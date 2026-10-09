import base64
import hashlib
import secrets
from urllib.parse import urlencode
import httpx
from app.core.config import settings


def create_pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge


def build_authorization_url(state: str, challenge: str) -> str:
    params = {
        "response_type": "code",
        "client_id": settings.X_CLIENT_ID,
        "redirect_uri": settings.X_REDIRECT_URI,
        "scope": settings.X_SCOPES,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return "https://twitter.com/i/oauth2/authorize?" + urlencode(params)


async def exchange_code(code: str, verifier: str) -> dict:
    raw = f"{settings.X_CLIENT_ID}:{settings.X_CLIENT_SECRET}".encode()
    auth = base64.b64encode(raw).decode()
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.X_REDIRECT_URI,
        "code_verifier": verifier,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.x.com/2/oauth2/token",
            data=data,
            headers={"Authorization": f"Basic {auth}"},
        )
    response.raise_for_status()
    return response.json()


async def get_me(access_token: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://api.x.com/2/users/me", headers={"Authorization": f"Bearer {access_token}"})
    response.raise_for_status()
    return response.json()


async def create_post(access_token: str, text: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.x.com/2/tweets",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"text": text},
        )
    response.raise_for_status()
    return response.json()
