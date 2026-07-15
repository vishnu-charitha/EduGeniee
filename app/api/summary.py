from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.auth.oauth import get_current_user
from app.database.models import User
from app.database.database import SessionLocal
from app.database import crud
from app.services.summary_service import generate_summary
from app.services.history_service import save_ai_history
router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)


class SummaryRequest(BaseModel):
    text: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def summary(request: SummaryRequest,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):

    query = crud.create_query(
        db=db,
        user_id=current_user.user_id,
        query_type="Summary",
        query_text=request.text
    )

    result = generate_summary(request.text)

    crud.save_summary(
        db=db,
        query_id=query.query_id,
        summary_text=result,
        summary_type="Educational"
    )

    save_ai_history(
        db=db,
        user_id=current_user.user_id,
        task="summary",
        prompt=request.text,
        response=result
    )

    return {
        "query_id": query.query_id,
        "summary": result
    }