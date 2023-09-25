import pytest
from sqlalchemy import select

from app.models import User
from app.tests.conftest import (
    client as test_client,
    create_sample_user,
)


@pytest.mark.asyncio
async def test_user_in_database(session):
    created_user = await create_sample_user(session)

    result = await session.execute(
        select(User).where(User.name == "SampleUser")
    )
    fetched_user = result.scalar_one_or_none()

    assert created_user is not None
    assert fetched_user is not None
    assert created_user.name == fetched_user.name
    assert created_user.age == fetched_user.age


@pytest.mark.parametrize(
    "data, expected_status",
    [
        ({"name": "Heorhii", "age": "123"}, 422),  # Not correct data
    ],
)
@pytest.mark.asyncio
async def test_create_user(test_client, session, data, expected_status):
    response = await test_client.post("/users/create_user/", json=data)
    assert response.status_code == expected_status
