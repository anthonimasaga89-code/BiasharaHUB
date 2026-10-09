from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.business import BusinessCreate, BusinessResponse, BusinessUpdate
from app.services.business_service import create_business, delete_business, get_business, get_my_businesses, update_business

router = APIRouter(prefix="/api/businesses", tags=["Businesses"])


@router.post("/", response_model=BusinessResponse, status_code=201)
def create(data: BusinessCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_business(db, data, current_user.id)


@router.get("/my", response_model=list[BusinessResponse])
def mine(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_my_businesses(db, current_user.id)


@router.get("/{business_id}", response_model=BusinessResponse)
def get_one(business_id: int, db: Session = Depends(get_db)):
    return get_business(db, business_id)


@router.patch("/{business_id}", response_model=BusinessResponse)
def update(business_id: int, data: BusinessUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_business(db, business_id, data, current_user.id)


@router.delete("/{business_id}")
def delete(business_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_business(db, business_id, current_user.id)
