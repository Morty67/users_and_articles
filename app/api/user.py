from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from app.auth.security import get_current_profile
from app.serializers.user_serializer import UserCreate, UserResponse
from app.services.user_service import UserService

from app.utils.dependencies.services import get_user_service


router = APIRouter()


@router.post("/create_user/", response_model=UserResponse)
async def create_user(
    item: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.create_user(item)


@router.get("/users_older_than/", response_model=List[UserResponse])
async def get_users_by_age(
    age_threshold: int, service: UserService = Depends(get_user_service)
):
    return await service.get_users_by_age(age_threshold)


@router.get("/users-by-color/", response_model=List[UserResponse])
async def get_users_by_color(
    color: str, service: UserService = Depends(get_user_service)
):
    return await service.get_users_by_color(color)


@router.get("/users-with-more-than-3-articles/")
async def get_users_with_more_than_3_articles(
    current_profile: dict = Depends(get_current_profile),
    service: UserService = Depends(get_user_service),
):
    return await service.get_users_with_more_than_3_articles()
