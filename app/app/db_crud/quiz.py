from app.models.quiz import Question, Quiz
from app.schemas.quiz import CreateQuizSchema
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD


class QuizCRUD(BaseCRUD[Quiz, CreateQuizSchema, CreateQuizSchema]):
    async def create(
        self,
        session: AsyncSession,
        in_obj: CreateQuizSchema,
        **attrs,
    ) -> Quiz:
        quiz_data = in_obj.dict()
        questions_data = quiz_data.pop("questions")

        quiz_data = jsonable_encoder(quiz_data)
        db_quiz = self.model(**quiz_data)
        session.add(db_quiz)

        for question_data in questions_data:
            question_data["quiz_id"] = db_quiz.id
            question_data = jsonable_encoder(question_data)
            db_question = Question(**question_data)
            session.add(db_question)

        await session.commit()
        await session.refresh(db_quiz)
        return db_quiz


quiz_db = QuizCRUD(Quiz)
