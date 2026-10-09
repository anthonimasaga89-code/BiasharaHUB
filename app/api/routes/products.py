from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import create_product, delete_product, get_active_products, get_business_products, get_product, update_product

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def catalog(db: Session = Depends(get_db)):
    return get_active_products(db)


@router.post("/business/{business_id}", response_model=ProductResponse, status_code=201)
def create(business_id: int, data: ProductCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_product(db, business_id, data, current_user.id)


@router.get("/business/{business_id}", response_model=list[ProductResponse])
def list_business(business_id: int, db: Session = Depends(get_db)):
    return get_business_products(db, business_id)


@router.get("/{product_id}", response_model=ProductResponse)
def get_one(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_product(db, product_id, data, current_user.id)


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_product(db, product_id, current_user.id)
