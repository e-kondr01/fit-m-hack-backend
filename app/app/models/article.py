from sqlalchemy import Column, String

from .base import Base


class Article(Base):
    title = Column(String, nullable=False)
    short_description = Column(String)
    tags = Column(String)
    image = Column(String)
