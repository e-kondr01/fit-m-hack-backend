from typing import Any

from app.db_crud import article_db
from app.deps import get_async_session
from app.schemas.article import ArticleSchema
from app.utils.get_topics import find_n_closest_topics, navec_model
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("", response_model=list[ArticleSchema])
async def get_recommended_articles(
    topic: str,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Список рекомендованных статей
    """
    closest_topics = find_n_closest_topics(
        topic, model=navec_model, show_similarity_values=False, n_topics=3
    )
    articles = []
    for topic in closest_topics:
        article = await article_db.get(session, tags=topic)
        articles.append(article)
    return articles
