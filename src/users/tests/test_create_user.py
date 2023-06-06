import http

from fastapi.testclient import TestClient

from src.main import app


class TestCreateUser:
    def test_crate_user_successful(self):
        client = TestClient(app)
        payload = {"username": "test@email.com", "password": "test123"}
        response = client.post(url="/api/v1/users/users/", data=payload)
        assert response.status_code == http.HTTPStatus.CREATED
        assert response.json() == {
            "id": 5,
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "role": 2,
            "username": "test@email.com",
        }

    def test_crate_existent_user(self):
        client = TestClient(app)
        payload = {"username": "test@email.com", "password": "test123"}
        response = client.post(url="/api/v1/users/users/", data=payload)
        assert response.status_code == http.HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "id": 5,
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "role": 2,
            "username": "test@email.com",
        }
