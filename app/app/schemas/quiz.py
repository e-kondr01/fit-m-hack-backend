from uuid import UUID

from pydantic import BaseModel


class QuestionSchema(BaseModel):
    id: UUID
    type: str
    text: str

    class Config:
        orm_mode = True


class QuizDetailSchema(BaseModel):
    id: UUID
    name: str
    questions: list[QuestionSchema]

    class Config:
        orm_mode = True


class QuizListSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
