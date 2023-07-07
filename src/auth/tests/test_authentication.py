import json
from http import HTTPStatus

import pytest


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_user_signin_successful(self, client, user_payload, customer):
        test_customer = await customer()
        response = await client.post(url="/api/v1/auth/signin/", data=user_payload)
        assert response.status_code == HTTPStatus.OK

        data = json.loads(response.content)
        assert data["id"] == test_customer.id

    @pytest.mark.asyncio
    async def test_user_signup_successful(self, client, user_payload):
        response = await client.post(url="/api/v1/auth/signup/", data=user_payload)
        assert response.status_code == HTTPStatus.CREATED
