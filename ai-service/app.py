from fastapi import FastAPI
from pydantic import BaseModel

from predict import predict_sentiment


app = FastAPI(
    title="ASG AI Service",
    description="Microservice de classification de sentiments géopolitiques",
    version="0.1.0"
)


class PredictionRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict")
def predict(request: PredictionRequest):
    result = predict_sentiment(request.text)
    return result