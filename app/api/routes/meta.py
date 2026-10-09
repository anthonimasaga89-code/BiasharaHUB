from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.frontend import redirect_to_frontend
from app.core.dependencies import get_current_user
from app.integrations.social.meta.client import graph_get
from app.integrations.social.meta.oauth import build_meta_authorization_url, exchange_meta_code
from app.integrations.social.linkedin.oauth import create_state, decode_state
from app.models.social_account import SocialAccount
from app.services.business_service import require_business_owner

router = APIRouter(prefix="/api/social/meta", tags=["Meta / Instagram / Facebook"])


@router.get("/connect")
def connect(
    business_id: int,
    format: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_business_owner(db, business_id, current_user.id)
    state = create_state(current_user.id, business_id)
    scopes = [item.strip() for item in settings.META_SCOPES.split(",") if item.strip()]
    authorization_url = build_meta_authorization_url(state, scopes)
    if format == "json":
        return {"authorization_url": authorization_url}
    return RedirectResponse(authorization_url)


@router.get("/callback")
async def callback(code: str | None = None, state: str | None = None, error: str | None = None, db: Session = Depends(get_db)):
    if error:
        raise HTTPException(400, f"Meta authorization failed: {error}")
    if not code or not state:
        raise HTTPException(400, "Missing Meta code or state")
    try:
        state_data = decode_state(state)
    except Exception:
        raise HTTPException(401, "Invalid OAuth state")

    token_data = await exchange_meta_code(code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(502, "Meta did not return an access token")

    profile = await graph_get("me", access_token, {"fields": "id,name"})
    account_id = profile.get("id")
    account_name = profile.get("name") or "Facebook Account"
    if not account_id:
        raise HTTPException(502, "Meta did not return an account identifier")

    business_id = int(state_data["business_id"])
    user_id = int(state_data["user_id"])
    require_business_owner(db, business_id, user_id)

    account = db.query(SocialAccount).filter(
        SocialAccount.business_id == business_id,
        SocialAccount.platform == "facebook",
        SocialAccount.account_id == account_id,
    ).first()
    if account:
        account.account_name = account_name
        account.access_token = access_token
        account.is_connected = True
    else:
        account = SocialAccount(
            business_id=business_id,
            platform="facebook",
            account_name=account_name,
            account_id=account_id,
            access_token=access_token,
            is_connected=True,
        )
        db.add(account)
    db.commit()

    await graph_get("me/accounts", access_token, {"fields": "id,name,access_token,instagram_business_account"})
    return redirect_to_frontend(connected="meta")


@router.post("/whatsapp/connect")
async def connect_whatsapp(business_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    require_business_owner(db, business_id, current_user.id)
    if not settings.WHATSAPP_ACCESS_TOKEN or not settings.WHATSAPP_BUSINESS_ACCOUNT_ID:
        raise HTTPException(503, "WhatsApp credentials are not configured")
    account = db.query(SocialAccount).filter(
        SocialAccount.business_id == business_id,
        SocialAccount.platform == "whatsapp",
        SocialAccount.account_id == settings.WHATSAPP_BUSINESS_ACCOUNT_ID,
    ).first()
    if account:
        account.access_token = settings.WHATSAPP_ACCESS_TOKEN
        account.is_connected = True
    else:
        account = SocialAccount(
            business_id=business_id,
            platform="whatsapp",
            account_name=f"WhatsApp Business {settings.WHATSAPP_BUSINESS_ACCOUNT_ID}",
            account_id=settings.WHATSAPP_BUSINESS_ACCOUNT_ID,
            access_token=settings.WHATSAPP_ACCESS_TOKEN,
            is_connected=True,
        )
        db.add(account)
    db.commit()
    return {"message": "WhatsApp Business account connected successfully"}
