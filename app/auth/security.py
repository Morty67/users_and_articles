from typing import Annotated
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.profile_model import Profile

from app.auth.token_serializer import TokenData
from app.utils.dependencies.get_session import get_session
from config import (
    pwd_context,
    oauth2_scheme,
    ALGORITHM,
    SECRET_KEY,
)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str):
    result = await session.execute(
        select(Profile).filter(Profile.username == username)
    )
    return result.scalar_one_or_none()


async def get_current_profile(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    profile = await get_user(session, username=token_data.username)
    if profile is None:
        raise credentials_exception
    return profile


async def get_current_active_profile(
    current_user: Annotated[Profile, Depends(get_current_profile)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
