from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.content import Content
from app.models.product import Product
from app.schemas.content import ContentCreate
from app.services.business_service import require_business_owner


def create_content(db: Session, business_id: int, data: ContentCreate, user_id: int):
    require_business_owner(db, business_id, user_id)
    if data.product_id:
        product = db.query(Product).filter(Product.id == data.product_id, Product.business_id == business_id).first()
        if not product:
            raise HTTPException(404, "Product not found in this business")
    status = "SCHEDULED" if data.scheduled_at else "DRAFT"
    content = Content(**data.model_dump(), business_id=business_id, status=status)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def get_content(db: Session, content_id: int):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(404, "Content not found")
    return content


def list_business_content(db: Session, business_id: int, user_id: int):
    require_business_owner(db, business_id, user_id)
    return db.query(Content).filter(Content.business_id == business_id).all()
