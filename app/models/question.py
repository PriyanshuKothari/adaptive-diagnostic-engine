from pydantic import BaseModel, Field
from typing import List, Optional


class Question(BaseModel):
    question_id: str
    text: str
    options: List[str]                  # ["A) ...", "B) ...", "C) ...", "D) ..."]
    correct_answer: str                 # e.g. "A"
    difficulty: float = Field(..., ge=0.1, le=1.0)
    topic: str                          # e.g. "Algebra", "Vocabulary"
    tags: List[str]                     # e.g. ["quadratic", "equations"]


class QuestionOut(BaseModel):
    """Safe version returned to student — no correct_answer."""
    question_id: str
    text: str
    options: List[str]
    difficulty: float
    topic: str
    tags: List[str]
