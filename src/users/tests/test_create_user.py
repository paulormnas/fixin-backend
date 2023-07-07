from http import HTTPStatus
import pytest

from src.core.models import UserRoleEnum


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_crate_customer_successful(self, client, user_payload, token):
        test_token = await token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 2,
            "role": UserRoleEnum.Customer.value,
            "username": user_payload["username"],
        }

    @pytest.mark.asyncio
    async def test_crate_existent_user(self, client, customer, user_payload, token):
        await customer()
        test_token = await token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
