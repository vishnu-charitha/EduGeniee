from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth.oauth import get_current_user
from app.auth.oauth import get_current_user
from app.database.database import SessionLocal
from app.database import crud, models

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):

    return {

        "questions": db.query(models.UserQuery).count(),

        "quizzes": db.query(models.Quiz).count(),

        "summaries": db.query(models.Summary).count(),

        "learning_paths": db.query(models.LearningPath).count()

    }
@router.get("/history")
def dashboard_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = crud.get_history(
        db,
        current_user.user_id
    )

    return [

        {

            "task": h.task,

            "prompt": h.prompt,

            "response": h.response,

            "created_at": h.created_at.strftime("%d %b %Y")

        }

        for h in history

    ]