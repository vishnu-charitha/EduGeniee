from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.database import crud

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

class QuizResult(BaseModel):

    user_id:int

    query_id:int

    score:int

    total_questions:int


def get_db():

    db=SessionLocal()

    try:

        yield db

    finally:

        db.close()


@router.post("/submit")

def submit(result:QuizResult,
           db:Session=Depends(get_db)):

    crud.save_quiz_attempt(

        db,

        result.user_id,

        result.query_id,

        result.score,

        result.total_questions

    )

    return {

        "message":"Quiz Saved"

    }