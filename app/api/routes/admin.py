from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import require_roles
from app.models.user import User
from app.models.business import Business
from app.models.order import Order
from app.core.database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/overview")
def overview(db: Session = Depends(get_db), current_user=Depends(require_roles("SUPER_ADMIN"))):
    return {
        "users": db.query(User).count(),
        "businesses": db.query(Business).count(),
        "orders": db.query(Order).count(),
    }
