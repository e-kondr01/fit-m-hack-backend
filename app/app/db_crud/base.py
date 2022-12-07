"""
Defines base class with generic logic for CRUD operations.
Every model should inherit this logic and enrich/override it if needed.
Notice: the CRUD functions DOES NOT validate the given input, therefore you
should validate the args before passing them to the CRUD functions.
"""

from typing import Any, Generic, Type, TypeVar, Union

from app.models import Base
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def create(
        self,
        session: AsyncSession,
        in_obj: CreateSchemaType,
        **attrs,
    ) -> ModelType:
        in_obj_data = jsonable_encoder(in_obj)
        attrs_data = jsonable_encoder(attrs)
        db_obj = self.model(**in_obj_data, **attrs_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(self, session: AsyncSession, **attrs) -> ModelType | None:
        statement = select(self.model).filter_by(**attrs)
        result = await session.execute(statement=statement)
        return result.scalars().first()

    async def exists(self, session: AsyncSession, **attrs) -> bool:
        statement = select(self.model.id).filter_by(**attrs)
        result = await session.execute(statement=statement)
        return result.first() is not None

    async def get_or_404(self, session: AsyncSession, **attrs) -> ModelType:
        db_obj = await self.get(session=session, **attrs)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__tablename__.capitalize()} not found",
            )
        return db_obj

    async def paginated_filter(
        self,
        session: AsyncSession,
        params: AbstractParams | None = None,
        order_by: str | None = None,
        **attrs,
    ) -> AbstractPage[ModelType]:
        query = select(self.model)
        order_by_expression = self.get_order_by_expression(order_by)
        filter_expression = self.get_filter_expression(**attrs)
        if filter_expression is not None:
            query = query.filter(filter_expression)
        if order_by_expression is not None:
            query = query.order_by(order_by_expression)
        return await paginate(session, query, params)

    def get_order_by_expression(self, order_by: str | None):
        if order_by:
            if order_by.startswith("-"):
                order_by = order_by[1:]
                expression = getattr(getattr(self.model, order_by), "desc")()
            else:
                expression = getattr(self.model, order_by)
        else:
            expression = None
        return expression

    def get_filter_expression(self, **kwargs):
        filters = []
        for key, value in kwargs.items():
            if value:
                # TODO: add other operators
                filters.append(getattr(getattr(self.model, key), "ilike")(f"%{value}%"))
        if filters:
            expression = filters[0]
            for filter_expression in filters[1:]:
                expression |= filter_expression
        else:
            expression = None
        return expression

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        in_obj: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(in_obj, dict):
            update_data = in_obj
        else:
            update_data = in_obj.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(
        self, session: AsyncSession, db_obj: ModelType
    ) -> ModelType | None:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
