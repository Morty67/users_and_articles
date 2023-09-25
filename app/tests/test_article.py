import pytest
from app.tests.conftest import client as test_client, create_sample_user


@pytest.mark.parametrize(
    "article_data, expected_status",
    [
        (
            {
                "text": "Lorem ipsum",
                "color": "white",
                "owner_name": "ValidName",
            },
            422,
        ),  # Not correct data
    ],
)
@pytest.mark.asyncio
async def test_create_article(
    test_client, session, article_data, expected_status
):
    sample_user = await create_sample_user(session)
    article_data["owner_name"] = sample_user.name
    response = await test_client.post(
        "/articles/create_article/", json=article_data
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_create_article_with_non_existing_user(test_client):
    response = await test_client.post(
        "/articles/create_article/",
        json={
            "text": "Lorem ipsum",
            "color": "red",
            "owner_name": "NonExistingUser",
        },
    )
    assert response.status_code == 404
