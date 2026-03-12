from fastapi import APIRouter, HTTPException
from app.models.session import SessionStart, SessionOut
from app.database import sessions_col
import uuid

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/start", response_model=SessionOut, status_code=201)
def start_session(body: SessionStart):
    """Create a new test session for a student."""
    session_id = str(uuid.uuid4())
    session_doc = {
        "session_id": session_id,
        "student_name": body.student_name,
        "ability": 0.5,
        "questions_asked": [],
        "answer_history": [],
        "is_complete": False,
        "started_at": __import__("datetime").datetime.utcnow(),
        "completed_at": None,
    }
    sessions_col.insert_one(session_doc)
    return SessionOut(
        session_id=session_id,
        student_name=body.student_name,
        ability=0.5,
        questions_answered=0,
        is_complete=False,
    )


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: str):
    """Fetch current session state."""
    doc = sessions_col.find_one({"session_id": session_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionOut(
        session_id=doc["session_id"],
        student_name=doc["student_name"],
        ability=doc["ability"],
        questions_answered=len(doc["questions_asked"]),
        is_complete=doc["is_complete"],
    )
