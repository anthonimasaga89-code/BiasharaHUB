from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.business_service import require_business_owner, get_business


def create_product(db: Session, business_id: int, data: ProductCreate, user_id: int):
    require_business_owner(db, business_id, user_id)
    product = Product(**data.model_dump(), business_id=business_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


def get_active_products(db: Session):
    return db.query(Product).filter(Product.status == "active").all()


def get_business_products(db: Session, business_id: int):
    get_business(db, business_id)
    return db.query(Product).filter(Product.business_id == business_id).all()


def update_product(db: Session, product_id: int, data: ProductUpdate, user_id: int):
    product = get_product(db, product_id)
    require_business_owner(db, product.business_id, user_id)
    if data.name is not None: product.name = data.name
    if data.description is not None: product.description = data.description
    if data.price is not None: product.price = data.price
    if data.stock is not None: product.stock = data.stock
    if data.location is not None: product.location = data.location
    if data.contact is not None: product.contact = data.contact
    if data.delivery_information is not None: product.delivery_information = data.delivery_information
    if data.image_url is not None: product.image_url = data.image_url
    if data.video_url is not None: product.video_url = data.video_url
    if data.status is not None: product.status = data.status
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int, user_id: int):
    product = get_product(db, product_id)
    require_business_owner(db, product.business_id, user_id)
    product.status = "inactive"
    db.commit()
    return {"message": "Product deactivated successfully"}
