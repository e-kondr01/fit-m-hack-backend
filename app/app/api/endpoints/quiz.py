import uuid
from typing import Any

from app.db_crud.quiz import quiz_db
from app.deps import get_async_session
from app.schemas.quiz import CreateQuizSchema, QuizDetailSchema, QuizListSchema
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "",
    response_model=Page[QuizListSchema],
)
async def get_quizzes(
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
) -> Any:
    """
    Получить список викторин.
    """
    quizzes = await quiz_db.paginated_filter(session, params=params)
    return quizzes


@router.get(
    "/{quiz_id}",
    response_model=QuizDetailSchema,
)
async def get_quiz(
    quiz_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Получить викторину с вопросами
    """
    quiz = await quiz_db.get_or_404(session, id=quiz_id)
    return quiz


@router.post("", response_model=QuizDetailSchema)
async def create_quiz(
    quiz_in: CreateQuizSchema, session: AsyncSession = Depends(get_async_session)
) -> Any:
    """
    Создание викторины
    """

    quiz = await quiz_db.create(session, quiz_in)
    return quiz
