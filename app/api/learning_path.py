from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.auth.oauth import get_current_user
from app.database.models import User
from app.database.database import SessionLocal
from app.database import crud
from app.services.learning_service import generate_learning_path
from app.services.history_service import save_ai_history
router = APIRouter(
    prefix="/learning-path",
    tags=["Learning Path"]
)


class LearningRequest(BaseModel):
    topic: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def learning_path(
    request: LearningRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = crud.create_query(
        db=db,
        user_id=current_user.user_id,
        query_type="Learning Path",
        query_text=request.topic
    )

    result = generate_learning_path(request.topic)

    crud.save_learning_path(
        db=db,
        query_id=query.query_id,
        topic=request.topic,
        difficulty_level="Beginner to Advanced",
        recommended_resources=result
    )
    save_ai_history(
        db=db,
        user_id=current_user.user_id,
        task="learning_path",
        prompt=request.topic,
        response=result
    )
    return {
        "query_id": query.query_id,
        "topic": request.topic,
        "learning_path": result
    }