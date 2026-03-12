from fastapi import FastAPI
from app.routes import sessions, questions, answers

app = FastAPI(
    title="Adaptive Diagnostic Engine",
    description="1D IRT-based adaptive testing system for GRE-style assessments",
    version="1.0.0",
)

app.include_router(sessions.router)
app.include_router(questions.router)
app.include_router(answers.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Adaptive Diagnostic Engine is running"}
