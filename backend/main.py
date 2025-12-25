from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import math
import os

# Initialize FastAPI
app = FastAPI()

# === Serve React frontend ===
frontend_build_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")

@app.get("/")
def serve_react():
    return FileResponse(os.path.join(frontend_build_path, "index.html"))

# === Backend API ===
class StudyCard(BaseModel):
    time_since_review: float  # hours
    confidence: float          # 0-1
    is_correct: bool

@app.post("/calculate")
def calculate(card: StudyCard):
    # 1. Base recall probability
    base = card.confidence if card.is_correct else card.confidence * 0.3

    # 2. Adjust for time since last review (exponential decay)
    recall_prob = base * math.exp(-0.05 * card.time_since_review)  # decay factor

    # 3. Cap recall probability between 0.01 and 0.99
    recall_prob = max(0.01, min(recall_prob, 0.99))

    # 4. Calculate next review hours (simpler SM-2 style)
    next_review_hours = 24 * (1 / recall_prob)  # scale factor
    next_review_hours = min(next_review_hours, 72)  # cap at 3 days

    # 5. Mistake type
    if card.is_correct:
        mistake_type = "none"
    elif card.confidence < 0.4:
        mistake_type = "guessing"
    else:
        mistake_type = "conceptual"

    return {
        "recall_probability": round(recall_prob, 2),
        "next_review_hours": round(next_review_hours, 1),
        "mistake_type": mistake_type
    }