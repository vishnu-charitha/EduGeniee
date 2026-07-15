from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.auth.oauth import get_current_user
from app.database.models import User
from app.database.database import SessionLocal
from app.database import crud
from app.services.ai_service import generate_ai_response
from app.services.history_service import save_ai_history
router = APIRouter(
    prefix="/ask",
    tags=["Question Answering"]
)


class QuestionRequest(BaseModel):
    question: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def ask(
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save User Query
    query = crud.create_query(
        db=db,
        user_id=current_user.user_id,
        query_type="Question Answering",
        query_text=request.question
    )

    # Generate AI Response
    answer = generate_ai_response(request.question)

    # Save AI Response
    crud.create_ai_response(
        db=db,
        query_id=query.query_id,
        response_text=answer,
        model_used="Gemini 3.5 Flash"
    )

    save_ai_history(
        db=db,
        user_id=current_user.user_id,
        task="question",
        prompt=request.question,
        response=answer
    )

    return {
        "question": request.question,
        "answer": answer
    }