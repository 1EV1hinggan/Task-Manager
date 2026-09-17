import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

DATABASE_URL = (
    "postgresql+psycopg://postgres:"
    f"{os.getenv('TEST_DB_PASSWORD')}@localhost/task_manager_test"
)

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def setup_test_database():
    Base.metadata.create_all(bind=engine)
