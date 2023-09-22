from fastapi import APIRouter, Depends
from app.services.article_service import ArticleService
from app.serializers.article_serializer import ArticleCreate, ArticleResponse
from app.utils.dependencies.services import get_article_service

router = APIRouter()


@router.post("/create_article/", response_model=ArticleResponse)
async def create_article(
    item: ArticleCreate,
    service: ArticleService = Depends(get_article_service),
):
    return await service.create_article(item)
