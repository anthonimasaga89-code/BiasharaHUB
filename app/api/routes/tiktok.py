from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.frontend import redirect_to_frontend
from app.core.security import create_access_token, decode_token
from app.integrations.social.tiktok.client import build_authorization_url, exchange_code, get_user_info
from app.integrations.social.linkedin.oauth import create_state, decode_state
from app.models.social_account import SocialAccount
from app.services.business_service import require_business_owner

router = APIRouter(prefix="/api/social/tiktok", tags=["TikTok"])


@router.get("/connect")
def connect(
    business_id: int,
    format: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_business_owner(db, business_id, current_user.id)
    state = create_state(current_user.id, business_id)
    authorization_url = build_authorization_url(state)
    if format == "json":
        return {"authorization_url": authorization_url}
    return RedirectResponse(authorization_url)


@router.get("/callback")
async def callback(code: str | None = None, state: str | None = None, error: str | None = None, db: Session = Depends(get_db)):
    if error:
        raise HTTPException(400, f"TikTok authorization failed: {error}")
    if not code or not state:
        raise HTTPException(400, "Missing TikTok code or state")
    try:
        state_data = decode_state(state)
    except Exception:
        raise HTTPException(401, "Invalid OAuth state")
    token_data = await exchange_code(code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(502, "TikTok did not return an access token")
    profile = await get_user_info(access_token)
    user_data = profile.get("data", {}).get("user", {})
    account_id = user_data.get("open_id") or user_data.get("union_id")
    account_name = user_data.get("display_name") or "TikTok Account"
    require_business_owner(db, int(state_data["business_id"]), int(state_data["user_id"]))
    account = SocialAccount(
        business_id=int(state_data["business_id"]),
        platform="tiktok",
        account_name=account_name,
        account_id=account_id,
        access_token=access_token,
        refresh_token=token_data.get("refresh_token"),
        is_connected=True,
    )
    db.add(account)
    db.commit()
    return redirect_to_frontend(connected="tiktok")
