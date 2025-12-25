from pydantic import BaseModel

class StudyCard(BaseModel):
    time_since_review: float  # hours
    confidence: float          # 0-1 scale
    is_correct: bool