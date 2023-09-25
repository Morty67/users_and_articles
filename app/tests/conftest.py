import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.auth.profile_model import Profile

from app.main import app
from app.models import Base, User
from config import DATABASE_URL_TEST

test_engine = create_async_engine(DATABASE_URL_TEST, echo=True, future=True)
test_async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # always drop and create test db tables between tests session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(
    test_db_setup_sessionmaker,
) -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session

        # delete all data from all tables after test
        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


async def create_sample_user(session):
    user = User(
        name="SampleUser",
        age=27,
    )
    session.add(user)
    await session.commit()
    return user


async def create_sample_profile(session):
    profile = Profile(
        username="SampleUser",
        email="user@example.com",
        full_name="Test User",
        hashed_password="password123",
    )
    session.add(profile)
    await session.commit()
    return profile
