from fastapi import APIRouter, Depends
from httpx import request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.database import crud
from app.services.explanation_service import generate_explanation
from app.auth.oauth import get_current_user
from app.database.models import User
from app.services.history_service import save_ai_history
router = APIRouter(
    prefix="/explain",
    tags=["Explanation"]
)


class ExplainRequest(BaseModel):
    topic: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def explain(
    request: ExplainRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = crud.create_query(
        db=db,
        user_id=current_user.user_id,
        query_type="Explanation",
        query_text=request.topic
    )

    answer = generate_explanation(request.topic)

    crud.create_ai_response(
        db=db,
        query_id=query.query_id,
        response_text=answer,
        model_used="Gemini 3.5 Flash"
    )

    save_ai_history(
        db=db,
        user_id=current_user.user_id,
        task="explanation",
        prompt=request.topic,
        response=answer
    )
    return {

    "topic": request.topic,

    "explanation": answer
    }