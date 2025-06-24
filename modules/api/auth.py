import os
import random
import string
import time
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from configs.api.users import config as users
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def authenticate_user(username: str, password: str):
    user = users.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data

def rotate_secret_key():
    """Rotate the secret key."""
    global SECRET_KEY
    new_secret_key = generate_secret_key()
    SECRET_KEY = new_secret_key
    print("Secret key rotated.")

def schedule_key_rotation(interval_seconds):
    """Schedule secret key rotation at regular intervals."""
    while True:
        rotate_secret_key()
        time.sleep(interval_seconds)

def generate_secret_key(length=32):
    """Generate a random string of letters and digits for the secret key."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

SECRET_KEY = os.environ.get("SECRET_KEY", None)
if SECRET_KEY is None:
    SECRET_KEY = generate_secret_key()
