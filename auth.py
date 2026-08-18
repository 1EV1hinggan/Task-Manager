from pwdlib import PasswordHash


import jwt
from datetime import datetime, timedelta, timezone



password_hash = PasswordHash.recommended()


SECRET_KEY = "development-secret-key-change-this-to-a-real-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(username):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )