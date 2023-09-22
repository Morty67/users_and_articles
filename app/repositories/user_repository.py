from typing import List

from sqlalchemy import select, func
from app.models import User, Article
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    async def get_users_by_age(self, age_threshold: int) -> List[User]:
        query = select(self.model).where(self.model.age > age_threshold)
        response = await self.session.execute(query)
        results = response.scalars().all()
        return results

    async def get_users_by_color(self, color: str) -> List[User]:
        query = select(User).join(Article).where(Article.color == color)
        response = await self.session.execute(query)
        results = response.scalars().all()
        return results

    async def get_users_with_more_than_3_articles(self) -> List[str]:
        subquery = (
            select(func.count(Article.id))
            .where(Article.owner_id == User.id)
            .label("article_count")
        )

        query = (
            select(User.name)
            .join(Article)
            .group_by(User.id)
            .having(func.count() > 3)
            .subquery()
        )

        response = await self.session.execute(select(query.c.name))
        results = [row[0] for row in response.all()]
        return results

    async def user_exists_by_name(self, name: str) -> bool:
        query = select(self.model).where(self.model.name == name)
        return await self.exists(query)
