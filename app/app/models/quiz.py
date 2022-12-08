from enum import StrEnum

from sqlalchemy import CheckConstraint, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Quiz(Base):
    """
    Викторина
    """

    name = Column(String, nullable=False)

    questions: list["Question"] = relationship(
        "Question", lazy="joined", order_by="Question.order"
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

    __table_args__: tuple = (
        CheckConstraint(order > 0, name="check_order_positive"),
        {},
    )

    feature = Column(String)

    min_label = Column(String)
    max_label = Column(String)

    # Ввод числа симптома
