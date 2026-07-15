from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database import crud, schemas, models
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.oauth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ----------------------------
# Database Dependency
# ----------------------------

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Register
# ----------------------------

@router.post("/register")
def register(

    user: schemas.UserCreate,

    db: Session = Depends(get_db)

):

    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:

        raise HTTPException(

            status_code=400,

            detail="Email already registered"

        )

    new_user = crud.create_user(db, user)

    return {

        "message": "Registration Successful",

        "user_id": new_user.user_id

    }


# ----------------------------
# Login
# ----------------------------

@router.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    user = db.query(models.User).filter(

        models.User.email == form_data.username

    ).first()

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid Email"

        )

    if not verify_password(

        form_data.password,

        user.password

    ):

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid Password"

        )

    access_token = create_access_token(

        data={

            "user_id": user.user_id,

            "email": user.email

        }

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }


# ----------------------------
# Current User
# ----------------------------

@router.get("/me")
def me(

    current_user: models.User = Depends(get_current_user)

):

    return {

        "user_id": current_user.user_id,

        "name": current_user.name,

        "email": current_user.email,

        "created_at": current_user.created_at

    }

@router.get("/me")
def get_me(

    current_user: models.User = Depends(get_current_user)

):

    return{

        "name":current_user.name,

        "email":current_user.email

    }