import http

from fastapi.testclient import TestClient

from src.main import app


class TestAuthentication:
    def test_authenticate_user_successful(self):
        client = TestClient(app)
        payload = {"username": "test@email.com", "password": "test123"}
        response = client.post(url="/api/v1/users/users/", data=payload)
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == {
            "id": 5,
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "role": 2,
            "username": "test@email.com",
        }
