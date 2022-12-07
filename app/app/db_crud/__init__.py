from app.models.quiz import Quiz
from app.schemas.quiz import QuizListSchema

from .base import BaseCRUD

# Implementation of "Repository" pattern
# Create new Database CRUD adapters like this:
# item_db = BaseCRUD[Item, CreateItemSchema, UpdateItemSchema](Item)
quiz_db = BaseCRUD[Quiz, QuizListSchema, QuizListSchema](Quiz)
