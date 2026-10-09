from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.frontend import redirect_to_frontend
from app.integrations.social.linkedin.oauth import build_authorization_url, create_state, decode_state, exchange_code
from app.integrations.social.linkedin.client import get_member_profile
from app.models.social_account import SocialAccount
from app.services.business_service import require_business_owner

router = APIRouter(prefix="/api/social/linkedin", tags=["LinkedIn"])


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
        raise HTTPException(400, f"LinkedIn authorization failed: {error}")
    if not code or not state:
        raise HTTPException(400, "Missing LinkedIn code or state")
    try:
        state_data = decode_state(state)
    except Exception:
        raise HTTPException(401, "Invalid OAuth state")
    token_data = await exchange_code(code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(502, "LinkedIn did not return an access token")
    profile = await get_member_profile(access_token)
    account_id = profile.get("sub") or profile.get("id")
    account_name = profile.get("name") or profile.get("given_name") or "LinkedIn Account"
    if not account_id:
        raise HTTPException(502, "LinkedIn profile did not return an account identifier")
    require_business_owner(db, int(state_data["business_id"]), int(state_data["user_id"]))
    account = db.query(SocialAccount).filter(
        SocialAccount.business_id == int(state_data["business_id"]),
        SocialAccount.platform == "linkedin",
        SocialAccount.account_id == account_id,
    ).first()
    if account:
        account.account_name = account_name
        account.access_token = access_token
        account.refresh_token = token_data.get("refresh_token")
        account.is_connected = True
    else:
        from datetime import datetime, timedelta
        account = SocialAccount(
            business_id=int(state_data["business_id"]),
            platform="linkedin",
            account_name=account_name,
            account_id=account_id,
            access_token=access_token,
            refresh_token=token_data.get("refresh_token"),
            token_expires_at=datetime.utcnow() + timedelta(seconds=int(token_data.get("expires_in", 0))) if token_data.get("expires_in") else None,
            is_connected=True,
        )
        db.add(account)
    db.commit()
    return redirect_to_frontend(connected="linkedin")
