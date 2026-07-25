from fastapi import FastAPI
from pydantic import BaseModel

from src.mindmate import analyze_message


app = FastAPI(
    title="MindMate API",
    description="Emotion-aware mental wellness API"
)


class MessageRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "MindMate API is running"
    }


@app.post("/analyze")
def analyze(request: MessageRequest):

    result = analyze_message(request.text)

    return result