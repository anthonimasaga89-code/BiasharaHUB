from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessUpdate


def create_business(db: Session, data: BusinessCreate, user_id: int):
    business = Business(**data.model_dump(), owner_id=user_id)
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


def get_business(db: Session, business_id: int):
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(404, "Business not found")
    return business


def get_my_businesses(db: Session, user_id: int):
    return db.query(Business).filter(Business.owner_id == user_id).all()


def require_business_owner(db: Session, business_id: int, user_id: int):
    business = get_business(db, business_id)
    if business.owner_id != user_id:
        raise HTTPException(403, "You are not allowed to manage this business")
    return business


def update_business(db: Session, business_id: int, data: BusinessUpdate, user_id: int):
    business = require_business_owner(db, business_id, user_id)
    if data.name is not None:
        business.name = data.name
    if data.description is not None:
        business.description = data.description
    if data.phone is not None:
        business.phone = data.phone
    if data.location is not None:
        business.location = data.location
    if data.status is not None:
        business.status = data.status
    db.commit()
    db.refresh(business)
    return business


def delete_business(db: Session, business_id: int, user_id: int):
    business = require_business_owner(db, business_id, user_id)
    business.status = "inactive"
    db.commit()
    return {"message": "Business deactivated successfully"}
