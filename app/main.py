from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.auth import router as auth_router
from app.api.routes import router
from app.api.pages import router as pages_router
from app.api.quiz_result import router as quiz_result_router
from app.api.analytics import router as analytics_router
from app.database.base import Base
from app.database.database import engine

# Import models so SQLAlchemy knows about them
from app.database.models import *
from app.core.exceptions import exception_handler
app = FastAPI(
    title="EduGenie Learning Assistant",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)
app.include_router(auth_router)
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)

app.include_router(pages_router)
app.include_router(quiz_result_router)
app.include_router(analytics_router)
app.add_exception_handler(
    Exception,
    exception_handler
)
@app.get("/")
def home():
    return {
        "message": "Welcome to EduGenie AI Learning Assistant"
    }