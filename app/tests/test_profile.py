import pytest
from sqlalchemy import select

from app.auth.profile_model import Profile
from app.tests.conftest import client as test_client, create_sample_profile


@pytest.mark.asyncio
async def test_profile_in_database(session):
    created_profile = await create_sample_profile(session)

    stmt = select(Profile).where(Profile.username == "SampleUser")
    result = await session.execute(stmt)
    fetched_profile = result.scalar_one_or_none()

    assert created_profile is not None
    assert fetched_profile is not None
    assert created_profile.username == fetched_profile.username
    assert created_profile.email == fetched_profile.email
    assert created_profile.full_name == fetched_profile.full_name
    assert created_profile.hashed_password == fetched_profile.hashed_password


@pytest.mark.parametrize(
    "profile_data, expected_status",
    [
        (
            {
                "username": 123,
                "email": "user1234@example.com",
                "full_name": "Test " "User",
                "hashed_password": "password123",
            },
            422,
        ),  # Not correct data
    ],
)
@pytest.mark.asyncio
async def test_create_profile(test_client, profile_data, expected_status):
    response = await test_client.post(
        "/profiles/create_profile/", json=profile_data
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_create_profile_with_not_unique_username_and_email(test_client):
    await test_client.post(
        "/profiles/create_profile/",
        json={
            "username": "TestUser",
            "email": "user123@example.com",
            "full_name": "Test User",
            "hashed_password": "password123",
        },
    )
    response = await test_client.post(
        "/profiles/create_profile/",
        json={
            "username": "TestUser",
            "email": "user123@example.com",
            "full_name": "Test User",
            "hashed_password": "password123",
        },
    )
    assert response.status_code == 400
