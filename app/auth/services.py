from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.profile_repository import ProfileRepository
from app.auth.profile_service import ProfileService
from app.utils.dependencies.get_session import get_session


def get_profile_service(
    session: AsyncSession = Depends(get_session),
) -> ProfileService:
    repo = ProfileRepository(session)
    service = ProfileService(profile_repo=repo)

    return service
