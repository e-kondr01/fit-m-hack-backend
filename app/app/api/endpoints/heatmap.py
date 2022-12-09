import uuid
from typing import Any

import pandas as pd
from app.db_crud.quiz import completed_quiz_db, quiz_db
from app.deps import get_async_session
from app.fastapi_users import current_user
from app.models.quiz import QuestionTypes
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
from sqlalchemy import Date, cast, func
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


def normalize(x, x_max, x_min):
    return (x - x_min) / (x_max - x_min)


@router.get(
    "/",
)
async def get_quiz_heatmap(
    session: AsyncSession = Depends(get_async_session),
    user_id: uuid.UUID | None = None,
) -> Any:
    """
    Получить список пройденных анкет
    """
    quizzes = await completed_quiz_db.filter_by(session, user_id=user_id)

    columns = []
    indexes = []
    data = []

    if quizzes:
        first_quiz = quizzes[0]
        columns.append(first_quiz.created_at)
        date_data = []
        for question in first_quiz.completed_questions:
            if question.type == QuestionTypes.RANGE:
                indexes.append(question.feature)
                norm_answer = normalize(
                    float(question.answer),
                    float(question.max_value),
                    float(question.min_value),
                )
                date_data.append(norm_answer)
        data.append(date_data)

        for quiz in quizzes:
            date_data = []
            columns.append(str(quiz.created_at).split(" ")[0])
            for question in quiz.completed_questions:
                if question.type == QuestionTypes.RANGE:
                    norm_answer = normalize(
                        float(question.answer),
                        float(question.max_value),
                        float(question.min_value),
                    )
                    date_data.append(norm_answer)
            data.append(date_data)

        # df = pd.DataFrame(index=['Симптом 1', 'Симптом 2', "Симп 3"],
        #          data=[[0.3, 0.2, 0.9],
        #                [0.1, 1.0, 0.9],
        #                [0.8, 0.7, 0.6]],
        #          columns=["2022-04-16", '2022-04-30', '2022-05-14'])
        return {"columns": columns, "indexes": indexes, "data": data}
    return {}
