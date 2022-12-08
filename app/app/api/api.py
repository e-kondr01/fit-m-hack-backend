from app.api.endpoints import article, auth, feature, quiz
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    quiz.router,
    prefix="/quiz",
    tags=["Викторины"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Авторизация"],
)

api_router.include_router(
    feature.router,
    prefix="/features",
    tags=["Симптомы"],
)

api_router.include_router(
    article.router,
    prefix="/articles",
    tags=["Статьи"],
)
