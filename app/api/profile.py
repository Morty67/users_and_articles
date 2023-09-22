from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.profile_model import Profile
from app.auth.profile_serializer import ProfileResponse, ProfileCreate
from app.auth.profile_service import ProfileService
from app.auth.security import get_current_active_profile

from app.auth.services import get_profile_service
from app.auth.token_serializer import Token


router = APIRouter()


@router.post("/create_profile/", response_model=ProfileResponse)
async def create_profile(
    item: ProfileCreate,
    service: ProfileService = Depends(get_profile_service),
):
    return await service.create_profile(item)


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: ProfileService = Depends(get_profile_service),
):
    access_token = await service.login(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=ProfileResponse)
async def read_users_me(
    current_user: Profile = Depends(get_current_active_profile),
):
    return current_user
