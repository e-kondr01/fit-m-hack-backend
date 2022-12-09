from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    short_description: str
    tags: str
    image: str | None

    class Config:
        orm_mode = True
