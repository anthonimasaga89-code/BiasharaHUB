from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import create_payment

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=201)
def create(data: PaymentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_payment(db, data, current_user.id)
