from app.models.quiz import Question, Quiz
from pydantic import BaseModel

from .base import BaseCRUD

# Implementation of "Repository" pattern
# Create new Database CRUD adapters like this:
# item_db = BaseCRUD[Item, CreateItemSchema, UpdateItemSchema](Item)
question_db = BaseCRUD[Question, BaseModel, BaseModel](Question)
