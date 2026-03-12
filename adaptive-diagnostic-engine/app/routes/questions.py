from fastapi import APIRouter, HTTPException
from app.models.question import QuestionOut
from app.database import questions_col, sessions_col
from app.services.irt import select_next_question

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/next", response_model=QuestionOut)
def get_next_question(session_id: str):
    """
    GET /questions/next?session_id=<id>
    Returns the optimal next question based on current ability (IRT selection).
    """
    session = sessions_col.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session["is_complete"]:
        raise HTTPException(status_code=400, detail="Session is already complete")

    all_questions = list(questions_col.find({}, {"_id": 0}))
    next_q = select_next_question(
        current_ability=session["ability"],
        all_questions=all_questions,
        asked_ids=session["questions_asked"],
    )

    if not next_q:
        raise HTTPException(status_code=404, detail="No more questions available")

    return QuestionOut(
        question_id=next_q["question_id"],
        text=next_q["text"],
        options=next_q["options"],
        difficulty=next_q["difficulty"],
        topic=next_q["topic"],
        tags=next_q["tags"],
    )
