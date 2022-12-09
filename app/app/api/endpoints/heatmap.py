import uuid
from typing import Any

import numpy as np
import pandas as pd
import seaborn as sns
from app.config import ROOT_DIR
from app.db_crud.quiz import completed_quiz_db
from app.deps import get_async_session
from app.models.quiz import QuestionTypes
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
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
        columns.append(str(first_quiz.created_at).split(".")[0])
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
            columns.append(str(quiz.created_at).split(".")[0])
            for question in quiz.completed_questions:
                if question.type == QuestionTypes.RANGE:
                    norm_answer = normalize(
                        float(question.answer),
                        float(question.max_value),
                        float(question.min_value),
                    )
                    date_data.append(norm_answer)
            data.append(date_data)

        print(indexes)
        print(data)
        data = np.array(data)
        data = np.transpose(data)
        print(columns)
        df = pd.DataFrame(index=indexes, data=data, columns=columns)

        heat = sns.heatmap(
            df,
            cmap=sns.color_palette("RdYlGn_r", 20, as_cmap=True),
            linewidths=5,
            vmin=0,
            vmax=0.99,
            cbar=False,
        )
        fig = heat.get_figure()
        fig.savefig(ROOT_DIR / "out.png", dpi=300)

        return FileResponse(ROOT_DIR / "out.png")
    return {}
