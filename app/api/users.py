from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database import crud, schemas

router = APIRouter(
    prefix="/users"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)