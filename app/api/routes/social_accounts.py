from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.social_account import SocialAccountResponse, SocialManualConnectRequest
from app.services.social_account_service import disconnect_social_account, get_business_social_accounts, save_social_account

router = APIRouter(prefix="/api/social-accounts", tags=["Social Accounts"])


@router.post("/{business_id}/manual", response_model=SocialAccountResponse)
def manual_connect(business_id: int, data: SocialManualConnectRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return save_social_account(db, business_id, data, current_user.id)


@router.get("/{business_id}", response_model=list[SocialAccountResponse])
def list_accounts(business_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_business_social_accounts(db, business_id, current_user.id)


@router.delete("/{account_id}")
def disconnect(account_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return disconnect_social_account(db, account_id, current_user.id)
