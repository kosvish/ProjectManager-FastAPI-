from pytest_mock import MockFixture
from tests.conftest import client
from tests.conftest import SessionLocal_test
from sqlalchemy import insert
from src.auth.models import Role


def test_add_role():
    with SessionLocal_test() as session:
        stmt = insert(Role).values(id=1, role_name="simple_user", permissions=None)
        session.execute(stmt)
        session.commit()


def test_registration(mocker: MockFixture):
    mocker.patch("src.auth.router.user_register")

    response = client.post("/auth/signup", json={"username": "user1", "email": "user111@example.com",
                                                 "password": "password", "role_id": 1})

    assert response.status_code == 201


def test_login(mocker: MockFixture):
    mocker.patch("src.auth.router.login_for_access_token")
    response = client.post("/auth/token", data={"username": "user1", "password": "password"})

    assert response.status_code == 200

