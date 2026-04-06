import uuid
import logging
from datetime import datetime, timedelta
from passlib.context import CryptContext
from src.config import config
import jwt
passwd_context =  CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )

    return token
    
def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
       
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


