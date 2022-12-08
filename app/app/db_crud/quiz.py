from app.db_crud import question_db
from app.models.quiz import CompletedQuestion, CompletedQuiz, Question, Quiz
from app.schemas.quiz import CreateCompletedQuizSchema, CreateQuizSchema
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
        await session.commit()

        for question_data in questions_data:
            question_data["quiz_id"] = db_quiz.id
            question_data = jsonable_encoder(question_data)
            db_question = Question(**question_data)
            session.add(db_question)

        await session.commit()
        await session.refresh(db_quiz)
        return db_quiz


quiz_db = QuizCRUD(Quiz)


class CompletedQuizCRUD(
    BaseCRUD[CompletedQuiz, CreateCompletedQuizSchema, CreateCompletedQuizSchema]
):
    async def create(
        self,
        session: AsyncSession,
        in_obj: CreateCompletedQuizSchema,
        **attrs,
    ) -> CompletedQuiz:
        quiz = await quiz_db.get_or_404(session, id=in_obj.quiz_id)

        completed_quiz_data = in_obj.dict()
        completed_quiz_data["name"] = quiz.name
        completed_questions_data = completed_quiz_data.pop("completed_questions")

        completed_quiz_data = jsonable_encoder(completed_quiz_data)
        attrs_data = jsonable_encoder(attrs)
        db_completed_quiz = self.model(**completed_quiz_data, **attrs_data)
        session.add(db_completed_quiz)
        await session.commit()

        for question_data in completed_questions_data:
            question = await question_db.get_or_404(
                session, id=question_data["question_id"]
            )
            question_data["completed_quiz_id"] = db_completed_quiz.id
            question_data["type"] = question.type
            question_data["text"] = question.text
            question_data["order"] = question.order
            question_data["feature"] = question.feature
            question_data["min_label"] = question.min_label
            question_data["max_label"] = question.max_label
            question_data["min_value"] = question.min_value
            question_data["max_value"] = question.max_value
            question_data = jsonable_encoder(question_data)
            db_completed_question = CompletedQuestion(**question_data)
            session.add(db_completed_question)

        await session.commit()
        await session.refresh(db_completed_quiz)
        return db_completed_quiz


completed_quiz_db = CompletedQuizCRUD(CompletedQuiz)
