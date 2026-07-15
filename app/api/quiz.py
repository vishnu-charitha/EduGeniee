from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.database import crud
from app.services.quiz_service import generate_quiz
from app.auth.oauth import get_current_user
from app.database.models import User
from app.services.history_service import save_ai_history
router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


class QuizRequest(BaseModel):
    topic: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def quiz(request: QuizRequest,
         db: Session = Depends(get_db),
         current_user: User = Depends(get_current_user)):

    query = crud.create_query(
        db=db,
        user_id=current_user.user_id,
        query_type="Quiz",
        query_text=request.topic
    )

    questions = generate_quiz(request.topic)

    for q in questions:

        crud.save_quiz(
    db=db,
    query_id=query.query_id,
    question_text=q["question"],
    option_a=q["option_a"],
    option_b=q["option_b"],
    option_c=q["option_c"],
    option_d=q["option_d"],
    correct_answer=q["correct_answer"]
)
    save_ai_history(

    db=db,
    user_id=current_user.user_id,
    task="quiz",
    prompt=request.topic,
    response=f"{len(questions)} questions generated"

)
    return {
        "query_id": query.query_id,
        "topic": request.topic,
        "quiz": questions
    }