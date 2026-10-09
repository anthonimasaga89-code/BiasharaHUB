from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.schemas.performance import PredictionRequest, PredictionResponse
from app.services.ml_service import predict_content

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])


@router.post("/predict", response_model=PredictionResponse)
def predict_endpoint(data: PredictionRequest, current_user=Depends(get_current_user)):
    return predict_content(data.model_dump())
