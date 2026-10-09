from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.business import Business
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


def create_order(db: Session, data: OrderCreate, customer_id: int):
    business = db.query(Business).filter(Business.id == data.business_id, Business.status == "active").first()
    if not business:
        raise HTTPException(404, "Business not found")
    order = Order(
        customer_id=customer_id,
        business_id=data.business_id,
        customer_phone=data.customer_phone,
        delivery_information=data.delivery_information,
        total_amount=Decimal("0"),
    )
    db.add(order)
    db.flush()
    total = Decimal("0")
    for item in data.items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.business_id == data.business_id,
            Product.status == "active",
        ).first()
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(409, f"Insufficient stock for product {product.name}")
        subtotal = product.price * item.quantity
        total += subtotal
        product.stock -= item.quantity
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=product.price, subtotal=subtotal))
    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order


def get_customer_orders(db: Session, customer_id: int):
    return db.query(Order).filter(Order.customer_id == customer_id).all()


def get_business_orders(db: Session, business_id: int, owner_id: int):
    business = db.query(Business).filter(Business.id == business_id, Business.owner_id == owner_id).first()
    if not business:
        raise HTTPException(403, "You are not allowed to view these orders")
    return db.query(Order).filter(Order.business_id == business_id).all()


def update_order_status(db: Session, order_id: int, status: str, owner_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    if order.business.owner_id != owner_id:
        raise HTTPException(403, "You are not allowed to update this order")
    allowed = {"PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"}
    if status not in allowed:
        raise HTTPException(400, "Invalid order status")
    order.status = status
    db.commit()
    db.refresh(order)
    return order
