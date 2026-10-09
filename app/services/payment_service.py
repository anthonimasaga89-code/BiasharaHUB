import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

SUPPORTED = {"mpesa", "airtel_money", "mixx", "halopesa", "card", "bank"}


def create_payment(db: Session, data: PaymentCreate, user_id: int):
    order = db.query(Order).filter(Order.id == data.order_id, Order.customer_id == user_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    if data.provider.lower() not in SUPPORTED:
        raise HTTPException(400, "Unsupported payment provider")
    if data.amount != order.total_amount:
        raise HTTPException(400, "Payment amount does not match order total")
    payment = Payment(
        order_id=order.id,
        provider=data.provider.lower(),
        reference=f"BH-{uuid.uuid4().hex[:20].upper()}",
        amount=data.amount,
        currency="TZS",
        status="PENDING",
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
