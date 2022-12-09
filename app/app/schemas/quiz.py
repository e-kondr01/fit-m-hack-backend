from datetime import date
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
    min_value: float | None
    max_value: float | None

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
    question_count: int


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


class CompletedQuestionDetailSchema(BaseModel):

    answer: str
    type: QuestionTypes
    text: str
    order: int
    feature: str | None
    min_label: str | None
    max_label: str | None
    min_value: float | None
    max_value: float | None

    class Config:
        orm_mode = True


class CompletedQuizDetailSchema(BaseModel):
    id: UUID
    name: str
    created_at: date
    questions: list[CompletedQuestionDetailSchema]

    class Config:
        orm_mode = True


class CompletedQuizListSchema(BaseModel):
    id: UUID
    name: str
    created_at: date

    class Config:
        orm_mode = True
