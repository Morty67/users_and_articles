from fastapi import HTTPException

from app.models import Article
from app.repositories.article_repository import ArticleRepository
from app.serializers.article_serializer import ArticleCreate, ArticleResponse


class ArticleService:
    def __init__(self, article_repo: ArticleRepository):
        self.article_repo = article_repo

    async def create_article(self, article_data: ArticleCreate):
        user = await self.article_repo.get_owner_for_article(
            article_data.owner_name
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with name {article_data.owner_name} not found",
            )

        article_data_dict = article_data.dict()
        del article_data_dict["owner_name"]

        article_data_dict["owner_id"] = user.id

        new_article = Article(**article_data_dict)
        await self.article_repo.save(new_article)

        return ArticleResponse(
            id=new_article.id,
            text=new_article.text,
            color=new_article.color,
            owner_name=article_data.owner_name,
        )
