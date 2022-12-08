from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from .base import Base

if TYPE_CHECKING:
    from app.models import User


class Quiz(Base):
    """
    Викторина
    """

    name = Column(String, nullable=False)

    questions: list["Question"] = relationship(
        "Question", lazy="joined", order_by="Question.order"
    )

    completed_quizzes: list["CompletedQuiz"] = relationship(
        "CompletedQuiz", lazy="joined"
    )


class CompletedQuiz(Base):
    """
    Заполненная викторина
    """

    name = Column(String, nullable=False)

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.id"), nullable=False)
    quiz: Quiz = relationship("Quiz", back_populates="completed_quizzes")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    user: "User" = relationship("User", lazy="joined")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    completed_questions: list["CompletedQuestion"] = relationship(
        "CompletedQuestion",
        lazy="joined",
        order_by="CompletedQuestion.order",
    )


class QuestionTypes(StrEnum):
    TEXTAREA = "textarea"
    RANGE = "range"


class Question(Base):
    """
    Вопрос викторины
    """

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.id"), nullable=False)
    quiz: Quiz = relationship("Quiz", back_populates="questions")

    type = Column(Enum(QuestionTypes), nullable=False)

    text = Column(String)

    order = Column(Integer)

    feature = Column(String)

    min_label = Column(String)
    max_label = Column(String)
    min_value = Column(Float)
    max_value = Column(Float)

    __table_args__: tuple = (
        CheckConstraint(order > 0, name="check_order_positive"),
        {},
    )

    # Ввод числа симптома


class CompletedQuestion(Base):

    completed_quiz_id = Column(
        UUID(as_uuid=True), ForeignKey("completedquiz.id"), nullable=False
    )
    completed_quiz: CompletedQuiz = relationship(
        "CompletedQuiz", back_populates="completed_questions"
    )

    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id"), nullable=False)
    question: Question = relationship("Question")

    answer = Column(String, nullable=False)

    type = Column(Enum(QuestionTypes), nullable=False)

    text = Column(String)

    order = Column(Integer)

    feature = Column(String)

    min_label = Column(String)
    max_label = Column(String)
    min_value = Column(Float)
    max_value = Column(Float)


Quiz.question_count = column_property(
    select(func.count(Question.id)).where(Question.quiz_id == Quiz.id).scalar_subquery()
)
