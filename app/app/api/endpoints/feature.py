from typing import Any

from app.db_crud import feature_db
from app.deps import get_async_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get(
    "",
)
async def get_features(
    name: str | None = None,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Список симптомов с фильтрацией
    """
    features = await feature_db.filter(session, name=name)
    resp = []
    for feature in features:
        resp.append(feature.name)
    return resp
