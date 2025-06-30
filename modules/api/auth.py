"""
Module contains functions to create and update secret key; generate and validate access tokens
"""

import os
import random
import string
import time
from typing import Union
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from configs.api.users import config as users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def authenticate_user(username: str, password: str) -> Union[False, dict]:
    """
    Check if user - password pair is correct
    :param username: Username
    :type username: str
    :param password: Password
    :type password: str
    :return: False if pair is incorrect, else - return user's dict
    :rtype: Union[False, dict]
    """
    user = users.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict) -> str:
    """
    Generate access token
    :param data: Dict (with user's data)
    :type data: dict
    :return: Generated token
    :rtype: str
    """
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get current user by token
    :param token: Access token
    :type token: str
    :return: User's info
    :rtype: dict
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from e
    return token_data

def rotate_secret_key() -> None:
    """
    Rotate the secret key
    """
    global SECRET_KEY
    new_secret_key = generate_secret_key()
    SECRET_KEY = new_secret_key
    print("Secret key rotated.")

def schedule_key_rotation(interval_seconds: int) -> None:
    """
    Schedule secret key rotation at regular intervals
    :param interval_seconds: Seconds between rotation intervals
    :type interval_seconds: int
    """
    while True:
        rotate_secret_key()
        time.sleep(interval_seconds)

def generate_secret_key(length: int = 32) -> str:
    """Generate a random string of letters and digits for the secret key.
    :param length: Length of secret key
    :type length: int
    :return: New secret key
    :rtype: str
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

SECRET_KEY = os.environ.get("SECRET_KEY", None)
if SECRET_KEY is None:
    SECRET_KEY = generate_secret_key()
