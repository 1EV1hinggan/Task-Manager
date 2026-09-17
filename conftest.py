import pytest

from test_database import TestingSessionLocal, setup_test_database
from models import User, Task


@pytest.fixture
def session():
    setup_test_database()

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()

        session.query(Task).delete()
        session.query(User).delete()

        session.commit()
        session.close()
