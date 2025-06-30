"""
Module with routes for authorize
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from modules.api.auth import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Generate an access token for an existing user
    :param form_data: User credentials
    :type form_data: OAuth2PasswordRequestForm
    :return: Token dict
    :rtype: dict
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token_data = {"sub": user["username"]}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
