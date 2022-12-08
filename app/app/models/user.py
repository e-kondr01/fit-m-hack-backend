from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from .base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore
    """
    Пользователь
    """

    role = Column(String, nullable=False)
