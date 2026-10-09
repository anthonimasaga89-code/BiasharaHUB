from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import create_order, get_business_orders, get_customer_orders, update_order_status

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create(data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_order(db, data, current_user.id)


@router.get("/my", response_model=list[OrderResponse])
def mine(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_customer_orders(db, current_user.id)


@router.get("/business/{business_id}", response_model=list[OrderResponse])
def business_orders(business_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_business_orders(db, business_id, current_user.id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_order_status(db, order_id, data.status, current_user.id)
