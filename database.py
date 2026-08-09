from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = (
    "postgresql+psycopg://postgres:"
    f"{os.getenv('DB_PASSWORD')}@localhost/task_manager"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)