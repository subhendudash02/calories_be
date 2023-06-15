"""
This file contains creation of jwt token based on the required payload
"""

from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError
from configparser import ConfigParser

config = ConfigParser()
config.read("./secrets.cfg")

expire_time = config["jwt"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
secret_key = config["jwt"]["SECRET_KEY"]


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=int(expire_time))

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")

    return encoded_jwt


def is_token_valid(token: str) -> bool:
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except ExpiredSignatureError:
        return False
    return True


def get_username(token: str) -> bool:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return payload.get("sub")
