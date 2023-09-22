from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.article_repository import ArticleRepository
from app.repositories.user_repository import UserRepository
from app.services.article_service import ArticleService
from app.services.user_service import UserService
from app.utils.dependencies.get_session import get_session


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    repo = UserRepository(session)
    service = UserService(user_repo=repo)

    return service


def get_article_service(
    session: AsyncSession = Depends(get_session),
) -> ArticleService:
    repo = ArticleRepository(session)
    service = ArticleService(article_repo=repo)
    return service
