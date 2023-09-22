from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from app.models import User
from app.repositories.user_repository import UserRepository


from app.serializers.user_serializer import UserCreate, UserResponse


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        query = select(User).where(User.name == user_data.name)
        if await self.user_repo.exists(query):
            raise HTTPException(
                detail="User with this name already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        new_user = User(**user_data.dict())
        await self.user_repo.save(new_user)

        return UserResponse(
            id=new_user.id, name=new_user.name, age=new_user.age
        )

    async def get_users_by_age(self, age_threshold: int) -> List[User]:
        return await self.user_repo.get_users_by_age(age_threshold)

    async def get_users_by_color(self, color: str) -> List[User]:
        return await self.user_repo.get_users_by_color(color)

    async def get_users_with_more_than_3_articles(self) -> List[str]:
        return await self.user_repo.get_users_with_more_than_3_articles()

    async def user_exists_by_name(self, name: str) -> bool:
        query = select(User).where(User.name == name)
        return await self.user_repo.exists(query)
