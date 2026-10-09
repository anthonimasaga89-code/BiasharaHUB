from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.performance import PerformanceCreate, PerformanceResponse
from app.services.analytics_service import create_performance, get_business_performance

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.post("/performance", response_model=PerformanceResponse, status_code=201)
def create(data: PerformanceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_performance(db, data, current_user.id)


@router.get("/business/{business_id}/performance", response_model=list[PerformanceResponse])
def performance(business_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_business_performance(db, business_id, current_user.id)
