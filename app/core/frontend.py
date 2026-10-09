from urllib.parse import urlencode

from fastapi.responses import RedirectResponse

from app.core.config import settings


def redirect_to_frontend(path: str = "/social", **params: str) -> RedirectResponse:
    query = f"?{urlencode(params)}" if params else ""
    return RedirectResponse(f"{settings.FRONTEND_URL.rstrip('/')}{path}{query}")
