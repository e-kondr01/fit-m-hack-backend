from app.models.feature import Feature
from app.models.quiz import Question
from app.models.user import User
from pydantic import BaseModel

from .base import BaseCRUD

# Implementation of "Repository" pattern
# Create new Database CRUD adapters like this:
# item_db = BaseCRUD[Item, CreateItemSchema, UpdateItemSchema](Item)
question_db = BaseCRUD[Question, BaseModel, BaseModel](Question)
feature_db = BaseCRUD[Feature, BaseModel, BaseModel](Feature)
user_db = BaseCRUD[User, BaseModel, BaseModel](User)
