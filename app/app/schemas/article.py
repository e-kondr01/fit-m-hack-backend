from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    short_description: str
    tags: str

    class Config:
        orm_mode = True
