from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.social_account import SocialAccount
from app.schemas.social_account import SocialManualConnectRequest
from app.services.business_service import require_business_owner

PLATFORMS = {"instagram", "facebook", "whatsapp", "tiktok", "linkedin", "x"}


def save_social_account(db: Session, business_id: int, data: SocialManualConnectRequest, user_id: int, token_expires_in: int | None = None):
    require_business_owner(db, business_id, user_id)
    platform = data.platform.lower()
    if platform not in PLATFORMS:
        raise HTTPException(400, "Unsupported platform")
    account = db.query(SocialAccount).filter(
        SocialAccount.business_id == business_id,
        SocialAccount.platform == platform,
        SocialAccount.account_id == data.account_id,
    ).first()
    expires = datetime.utcnow() + timedelta(seconds=token_expires_in) if token_expires_in else None
    if account:
        account.account_name = data.account_name
        account.access_token = data.access_token
        account.refresh_token = data.refresh_token
        account.token_expires_at = expires
        account.is_connected = True
    else:
        account = SocialAccount(
            business_id=business_id,
            platform=platform,
            account_name=data.account_name,
            account_id=data.account_id,
            access_token=data.access_token,
            refresh_token=data.refresh_token,
            token_expires_at=expires,
            is_connected=True,
        )
        db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_business_social_accounts(db: Session, business_id: int, user_id: int):
    require_business_owner(db, business_id, user_id)
    return db.query(SocialAccount).filter(SocialAccount.business_id == business_id).all()


def disconnect_social_account(db: Session, account_id: int, user_id: int):
    account = db.query(SocialAccount).filter(SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(404, "Social account not found")
    require_business_owner(db, account.business_id, user_id)
    account.is_connected = False
    db.commit()
    return {"message": "Social account disconnected successfully"}
