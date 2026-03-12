from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import questions_col, sessions_col
from app.services.irt import update_ability, session_is_complete
from app.services.llm import generate_study_plan
from app.models.session import AnswerRecord

router = APIRouter(prefix="/answers", tags=["Answers"])


class SubmitAnswer(BaseModel):
    session_id: str
    question_id: str
    selected_answer: str        # e.g. "A", "B", "C", or "D"


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    new_ability: float
    questions_answered: int
    is_complete: bool
    study_plan: Optional[str] = None    # Only present when session ends


@router.post("/submit", response_model=AnswerResponse)
def submit_answer(body: SubmitAnswer):
    """
    POST /answers/submit
    Evaluates the answer, updates ability via IRT, and checks if session ends.
    If session ends (10 questions), triggers Groq study plan generation.
    """
    # Fetch session
    session = sessions_col.find_one({"session_id": body.session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["is_complete"]:
        raise HTTPException(status_code=400, detail="Session already complete")

    # Fetch question
    question = questions_col.find_one({"question_id": body.question_id}, {"_id": 0})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Evaluate answer
    is_correct: bool = body.selected_answer.strip().upper() == question["correct_answer"].strip().upper()

    # IRT ability update
    new_ability: float = update_ability(
        theta=session["ability"],
        difficulty=question["difficulty"],
        is_correct=is_correct,
    )

    # Build answer record
    record = {
        "question_id": body.question_id,
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "is_correct": is_correct,
        "ability_after": new_ability,
    }

    # Update session in DB
    updated_asked = session["questions_asked"] + [body.question_id]
    updated_history = session["answer_history"] + [record]
    complete = session_is_complete(len(updated_asked))

    update_fields = {
        "ability": new_ability,
        "questions_asked": updated_asked,
        "answer_history": updated_history,
        "is_complete": complete,
    }
    if complete:
        update_fields["completed_at"] = datetime.utcnow()

    sessions_col.update_one({"session_id": body.session_id}, {"$set": update_fields})

    # Generate study plan if session just completed
    study_plan: Optional[str] = None
    if complete:
        try:
            answer_records = [AnswerRecord(**r) for r in updated_history]
            study_plan = generate_study_plan(new_ability, answer_records)
        except Exception as e:
            study_plan = f"Study plan generation failed: {str(e)}"

    return AnswerResponse(
        is_correct=is_correct,
        correct_answer=question["correct_answer"],
        new_ability=new_ability,
        questions_answered=len(updated_asked),
        is_complete=complete,
        study_plan=study_plan,
    )
