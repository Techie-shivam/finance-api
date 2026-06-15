# src/api/serve.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from src.monitoring.monitor import log_prediction   # ✅ import at top

app = FastAPI(title="Finance Transaction Classifier")

# Load model once at startup
model = joblib.load("src/models/category_model.pkl")


class Transaction(BaseModel):
    description: str


class Prediction(BaseModel):
    description: str
    category: str


@app.get("/")
def root():
    return {"message": "Finance Classifier API is running 🚀"}


@app.post("/predict", response_model=Prediction)
def predict(transaction: Transaction):
    category = model.predict([transaction.description])[0]
    log_prediction(transaction.description, category)   # ✅ log it
    return Prediction(
        description=transaction.description,
        category=category
    )                                                   # ✅ no stray )


@app.post("/predict-batch")
def predict_batch(transactions: list[Transaction]):
    descriptions = [t.description for t in transactions]
    categories = model.predict(descriptions)

    for d, c in zip(descriptions, categories):         # ✅ log batch too
        log_prediction(d, c)

    return [
        {"description": d, "category": c}
        for d, c in zip(descriptions, categories)
    ]

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}