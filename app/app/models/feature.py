from sqlalchemy import Column, String

from .base import Base


class Feature(Base):
    name = Column(String, nullable=False)
