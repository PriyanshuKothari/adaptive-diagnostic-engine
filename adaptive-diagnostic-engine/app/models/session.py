from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class AnswerRecord(BaseModel):
    question_id: str
    topic: str
    difficulty: float
    is_correct: bool
    ability_after: float                # theta after this question


class UserSession(BaseModel):
    session_id: str
    student_name: str
    ability: float = 0.5                # theta — starts at baseline 0.5
    questions_asked: List[str] = []     # list of question_ids already shown
    answer_history: List[AnswerRecord] = []
    is_complete: bool = False
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class SessionStart(BaseModel):
    student_name: str


class SessionOut(BaseModel):
    session_id: str
    student_name: str
    ability: float
    questions_answered: int
    is_complete: bool
