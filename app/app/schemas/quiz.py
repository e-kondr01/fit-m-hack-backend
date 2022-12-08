from uuid import UUID

from pydantic import BaseModel


class BaseQuestionSchema(BaseModel):
    type: str
    text: str

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
