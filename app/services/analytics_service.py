from sqlalchemy.orm import Session
from app.models.content import Content
from app.models.performance import PerformanceData
from app.schemas.performance import PerformanceCreate
from app.services.business_service import require_business_owner


def create_performance(db: Session, data: PerformanceCreate, user_id: int):
    content = db.query(Content).filter(Content.id == data.content_id).first()
    if not content:
        from fastapi import HTTPException
        raise HTTPException(404, "Content not found")
    require_business_owner(db, content.business_id, user_id)
    record = PerformanceData(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_business_performance(db: Session, business_id: int, user_id: int):
    require_business_owner(db, business_id, user_id)
    return db.query(PerformanceData).join(Content).filter(Content.business_id == business_id).all()
