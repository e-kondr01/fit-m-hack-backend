import uuid
from datetime import date

from fastapi_users import schemas
from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    role: str
    name: str
    birthdate: date
    diagnosis: str


class UserRead(schemas.BaseUser[uuid.UUID], BaseUserSchema):
    pass


class UserCreate(schemas.BaseUserCreate, BaseUserSchema):
    pass


class UserUpdate(schemas.BaseUserUpdate, BaseUserSchema):
    pass
