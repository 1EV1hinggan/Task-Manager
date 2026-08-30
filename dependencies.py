from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy import select

from auth import SECRET_KEY, ALGORITHM
from database import SessionLocal
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    with SessionLocal() as session:
        statement = select(User).where(User.id == user_id)
        user = session.scalars(statement).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user