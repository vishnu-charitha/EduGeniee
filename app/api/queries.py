from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database import crud, schemas

router = APIRouter(
    prefix="/queries"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_query(
    query: schemas.UserQueryCreate,
    db: Session = Depends(get_db)
):

    return crud.create_query(db, query)