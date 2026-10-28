import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import get_db
from main import app

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL não configurada")

test_engine = create_engine(TEST_DATABASE_URL)

if test_engine.url.database != "taskflow_test":
    raise RuntimeError("Os testes devem usar exclusivamente o banco taskflow_test")

@pytest.fixture
def db_connection():
    with test_engine.connect() as connection:
        transaction = connection.begin()

        yield connection

        transaction.rollback()


@pytest.fixture
def override_db(db_connection):
    def get_test_db():
        with Session(
            bind=db_connection,
            join_transaction_mode="create_savepoint"
        ) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    yield

    app.dependency_overrides.pop(get_db, None)