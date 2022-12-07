from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Quiz(Base):
    """
    Викторина
    """

    name = Column(String, nullable=False)

    questions: list["Question"] = relationship("Question", lazy="joined")


class Question(Base):
    """
    Вопрос викторины
    """

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quiz.id"), nullable=False)
    quiz: Quiz = relationship("Quiz", back_populates="questions")

    type = Column(String, nullable=False)

    text = Column(String)
