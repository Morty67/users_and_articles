from typing import Optional

from sqlalchemy import select

from app.models import Article, User
from app.repositories.base import BaseRepository


class ArticleRepository(BaseRepository):
    model = Article

    async def get_owner_for_article(self, name: str) -> Optional[User]:
        query = select(User).where(User.name == name)
        response = await self.session.execute(query)
        user = response.scalar()
        return user
