from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.profile_model import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, obj: Any):
        self.session.add(obj)
        await self.session.commit()

    async def get_user(self, username: str):
        result = await self.execute(
            select(Profile).filter(Profile.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Profile:
        result = await self.session.execute(
            select(Profile).filter(Profile.username == username)
        )
        return result.scalar_one_or_none()

    async def exists_by_username(self, username: str) -> bool:
        query = select(Profile).where(Profile.username == username)
        result = await self.session.execute(query)
        return result.scalar() is not None

    async def exists_by_email(self, email: str) -> bool:
        query = select(Profile).where(Profile.email == email)
        result = await self.session.execute(query)
        return result.scalar() is not None
