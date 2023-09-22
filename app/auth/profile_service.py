from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt

from starlette import status

from app.auth.profile_model import Profile
from app.auth.profile_repository import ProfileRepository
from app.auth.profile_serializer import ProfileCreate, ProfileResponse

from config import password_context, SECRET_KEY, ALGORITHM


class ProfileService:
    def __init__(self, profile_repo: ProfileRepository):
        self.profile_repo = profile_repo

    async def create_profile(
        self, profile_data: ProfileCreate
    ) -> ProfileResponse:
        if await self.profile_repo.exists_by_username(profile_data.username):
            raise HTTPException(
                detail="User with this name or email already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if await self.profile_repo.exists_by_email(profile_data.email):
            raise HTTPException(
                detail="User with this name or email already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        hashed_password = password_context.hash(profile_data.hashed_password)

        new_profile = Profile(
            username=profile_data.username,
            email=profile_data.email,
            full_name=profile_data.full_name,
            hashed_password=hashed_password,
        )

        await self.profile_repo.save(new_profile)
        return ProfileResponse(
            id=new_profile.id,
            username=new_profile.username,
            email=new_profile.email,
            full_name=new_profile.full_name,
            hashed_password=new_profile.hashed_password,
            disabled=new_profile.disabled,
        )

    async def login(self, username: str, password: str) -> str:
        profile = await self.profile_repo.get_by_username(username)
        if not profile or not await self.verify_password(
            password, profile.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await self.create_jwt_token(
            data={"sub": profile.username}
        )
        return access_token

    async def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return password_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, username: str, password: str) -> str:
        profile = await self.profile_repo.get_by_username(username)
        if not profile or not await self.verify_password(
            password, profile.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await self.create_jwt_token(
            data={"sub": profile.username}
        )
        return access_token

    async def create_jwt_token(
        self, data: dict, expires_minutes: int = 30
    ) -> str:
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
