from app.api.endpoints import quiz
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(
    quiz.router,
    prefix="/quiz",
    tags=["Викторины"],
)
