from sqlalchemy import select

from models import User
from auth import hash_password


def create_user(session, username, password):
    hashed_password = hash_password(password)

    user = User(
        username=username,
        password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_username(session, username):
    statement = select(User).where(User.username == username)

    return session.scalars(statement).first()