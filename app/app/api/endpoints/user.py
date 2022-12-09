from typing import Any

from app.db_crud import user_db
from app.deps import get_async_session
from app.schemas.user import UserRead
from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "",
    response_model=Page[UserRead],
)
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    params: Params = Depends(),
) -> Any:
    """
    Получить список пациентов
    """
    users = await user_db.paginated_filter(session, params=params)
    return users
