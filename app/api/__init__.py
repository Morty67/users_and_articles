from fastapi import APIRouter

from app.api.article import router as article_router
from app.api.user import router as user_router
from app.api.profile import router as profile_router


api_router = APIRouter()

api_router.include_router(
    article_router, prefix="/articles", tags=["Article"]
)
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(
    profile_router, prefix="/profiles", tags=["Profile"]
)
