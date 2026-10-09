from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.integrations.social.x.client import build_authorization_url, create_pkce, exchange_code, get_me
from app.integrations.social.linkedin.oauth import create_state, decode_state
import jwt
from app.core.config import settings
from app.core.frontend import redirect_to_frontend
from datetime import datetime, timedelta, timezone
from app.models.social_account import SocialAccount
from app.services.business_service import require_business_owner

router = APIRouter(prefix="/api/social/x", tags=["X"])


@router.get("/connect")
def connect(
    business_id: int,
    format: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_business_owner(db, business_id, current_user.id)
    verifier, challenge = create_pkce()
    payload = {"user_id": current_user.id, "business_id": business_id, "verifier": verifier, "exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
    state = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    url = build_authorization_url(state, challenge)
    if format == "json":
        return {"authorization_url": url}
    return RedirectResponse(url)


@router.get("/callback")
async def callback(code: str | None = None, state: str | None = None, db: Session = Depends(get_db)):
    if not code or not state:
        raise HTTPException(400, "Missing X authorization code or state")
    try:
        state_data = jwt.decode(state, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(401, "Invalid OAuth state")
    token_data = await exchange_code(code, state_data["verifier"])
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(502, "X did not return an access token")
    profile = await get_me(access_token)
    user_data = profile.get("data", {})
    account_id = user_data.get("id")
    account_name = user_data.get("name") or user_data.get("username") or "X Account"
    require_business_owner(db, int(state_data["business_id"]), int(state_data["user_id"]))
    account = SocialAccount(business_id=int(state_data["business_id"]), platform="x", account_name=account_name, account_id=account_id, access_token=access_token, refresh_token=token_data.get("refresh_token"), is_connected=True)
    db.add(account)
    db.commit()
    return redirect_to_frontend(connected="x")
