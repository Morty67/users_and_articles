from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_auth_access_token_fail_no_user(client: AsyncClient):
    response = await client.post(
        "/profiles/login/",
        data={
            "username": "xxx",
            "password": "yyy",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
