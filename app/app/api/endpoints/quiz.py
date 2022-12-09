import uuid
from typing import Any

from app.db_crud.quiz import completed_quiz_db, quiz_db
from app.deps import get_async_session
from app.fastapi_users import current_user
from app.models.user import User
from app.schemas.quiz import (
    CompletedQuizDetailSchema,
    CompletedQuizListSchema,
    CreateCompletedQuizSchema,
    CreateQuizSchema,
    QuizDetailSchema,
    QuizListSchema,
)
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


@router.post("/completed/", response_model=CreateCompletedQuizSchema)
async def create_completed_quiz(
    completed_quiz_in: CreateCompletedQuizSchema,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    """
    Создание пройденной анкеты
    """

    completed_quiz = await completed_quiz_db.create(
        session, completed_quiz_in, user_id=user.id
    )
    return completed_quiz


@router.get(
    "/completed",
    response_model=Page[CompletedQuizListSchema],
)
async def get_completed_quizzes(
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
) -> Any:
    """
    Получить списка пройденных анкет
    """
    quizzes = await completed_quiz_db.paginated_filter(session, params=params)
    return quizzes


@router.get(
    "/completed/{quiz_id}",
    response_model=CompletedQuizDetailSchema,
)
async def get_quiz(
    quiz_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Получить пройденную викторину
    """
    quiz = await completed_quiz_db.get_or_404(session, id=quiz_id)
    return quiz
