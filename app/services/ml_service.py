from fastapi import HTTPException
from app.ml.pipeline import predict


def predict_content(data: dict):
    try:
        value = predict(data)
    except FileNotFoundError as exc:
        raise HTTPException(503, str(exc))
    return {"predicted_performance": value, "model": "RandomForestRegressor", "trained": True}
