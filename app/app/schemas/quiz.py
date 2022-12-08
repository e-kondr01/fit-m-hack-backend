from uuid import UUID

from app.models.quiz import QuestionTypes
from pydantic import BaseModel, PositiveInt


class BaseQuestionSchema(BaseModel):
    type: QuestionTypes
    text: str
    order: PositiveInt
    feature: str | None
    min_label: str | None
    max_label: str | None

    class Config:
        orm_mode = True


class RetrieveQuestionSchema(BaseQuestionSchema):
    id: UUID


class BaseQuizSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class QuizDetailSchema(BaseQuizSchema):
    id: UUID
    questions: list[RetrieveQuestionSchema]


class QuizListSchema(BaseQuizSchema):
    id: UUID


class CreateQuizSchema(BaseQuizSchema):
    questions: list[BaseQuestionSchema]


class CreateCompletedQuestionSchema(BaseModel):
    question_id: UUID
    answer: str

    class Config:
        orm_mode = True


class CreateCompletedQuizSchema(BaseModel):
    quiz_id: UUID
    completed_questions: list[CreateCompletedQuestionSchema]

    class Config:
        orm_mode = True
