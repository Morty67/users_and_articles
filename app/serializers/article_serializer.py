from pydantic import BaseModel

from app.models.article import Article


class ArticleCreate(BaseModel):
    text: str
    color: Article.ColorEnum
    owner_name: str


class ArticleResponse(BaseModel):
    id: int
    text: str
    color: Article.ColorEnum
    owner_name: str
