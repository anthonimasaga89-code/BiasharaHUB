from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

MODEL_PATH = Path("ml_models/content_performance.joblib")


def train_model(rows: list[dict]) -> dict:
    if len(rows) < 10:
        raise ValueError("At least 10 historical records are required for a baseline model")
    df = pd.DataFrame(rows)
    target = "target"
    features = ["platform", "content_length", "hashtag_count", "hour", "day_of_week", "historical_engagement"]
    if not set(features + [target]).issubset(df.columns):
        raise ValueError("Training data is missing required features")
    X = df[features]
    y = df[target]
    preprocessor = ColumnTransformer(
        transformers=[("platform", OneHotEncoder(handle_unknown="ignore"), ["platform"])],
        remainder="passthrough",
    )
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestRegressor(n_estimators=200, random_state=42))
    ])
    pipeline.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    return {"model": str(MODEL_PATH), "rows": len(df)}


def predict(features: dict) -> float:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("ML model has not been trained")
    model = joblib.load(MODEL_PATH)
    frame = pd.DataFrame([features])
    return float(model.predict(frame)[0])
