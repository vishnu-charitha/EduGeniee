from fastapi import APIRouter

from app.api.users import router as user_router
from app.api.queries import router as query_router
from app.api.quiz import router as quiz_router
from app.api.summary import router as summary_router
from app.api.learning_path import router as learning_router
from app.api.ask import router as ask_router
from app.api.explain import router as explain_router
from app.api.pages import router as page_router
from app.api.dashboard import router as dashboard_router

router = APIRouter()
router.include_router(page_router)
router.include_router(user_router, tags=["Users"])

router.include_router(query_router, tags=["Queries"])

router.include_router(quiz_router, tags=["Quiz"])

router.include_router(summary_router, tags=["Summary"])

router.include_router(learning_router, tags=["Learning Path"])
router.include_router(dashboard_router)
router.include_router(ask_router)

router.include_router(explain_router)