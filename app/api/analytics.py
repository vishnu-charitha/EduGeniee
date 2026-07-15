from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import SessionLocal
from app.database import models
from app.auth.oauth import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def analytics(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    question_count = db.query(models.History).filter(
        models.History.user_id == current_user.user_id,
        models.History.task == "question"
    ).count()

    quiz_count = db.query(models.History).filter(
        models.History.user_id == current_user.user_id,
        models.History.task == "quiz"
    ).count()

    summary_count = db.query(models.History).filter(
        models.History.user_id == current_user.user_id,
        models.History.task == "summary"
    ).count()

    learning_count = db.query(models.History).filter(
        models.History.user_id == current_user.user_id,
        models.History.task == "learning"
    ).count()

    average_score = db.query(
        func.avg(models.QuizAttempt.score)
    ).filter(
        models.QuizAttempt.user_id == current_user.user_id
    ).scalar() or 0

    return {

        "questions": question_count,
        "quizzes": quiz_count,
        "summaries": summary_count,
        "learning_paths": learning_count,
        "average_score": round(average_score,2)

    }