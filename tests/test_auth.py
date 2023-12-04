from fastapi.testclient import TestClient
from pytest_mock import MockFixture
from main import app
from src.auth.router import user_register

client = TestClient(app)


def test_registration(mocker: MockFixture):
    mocker.patch("src.auth.router.user_register")

    # Тестирование успешной регистрации
    response = client.post("/auth/signup",
                           json={"username": "user1", "email": "user111@example.com", "password": "password"})
    assert response.status_code == 201


