from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, Date, String

from .base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore
    """
    Пользователь
    """

    role = Column(String, nullable=False)
    birthdate = Column(Date)
    name = Column(String)
    diagnosis = Column(String)
