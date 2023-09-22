from fastapi import FastAPI

from app.api import api_router
from app.core.database import engine, Base
from app.utils.data_genertor import generate_random_data

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await generate_random_data()
