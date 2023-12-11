import pytest
from fastapi.testclient import TestClient
from src.database import Base, get_db
from sqlalchemy.orm import sessionmaker
from main import app
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from src.config import DB_TEST_NAME, DB_TEST_PORT, DB_TEST_HOST, DB_TEST_PASSWORD, DB_TEST_USER
import pdb



TEST_DATABASE_URL = f"postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}"
engine_test = create_engine(TEST_DATABASE_URL, poolclass=NullPool)
SessionLocal_test = sessionmaker(bind=engine_test, expire_on_commit=False)
Base.metadata.bind = engine_test

client = TestClient(app)


def override_get_db():
    try:
        db = SessionLocal_test()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="session")
def prepare_database():
    try:
        Base.metadata.create_all(bind=engine_test)
        yield
    finally:
        Base.metadata.drop_all(bind=engine_test)




