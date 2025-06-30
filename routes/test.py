"""
Module with test routes
"""

from fastapi import APIRouter, Depends
from modules.api.auth import get_current_user

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

@router.get("")
async def test() -> dict:
    """
    Test connection
    :return: Test dict
    :rtype: dict
    """
    return {"status": "ok"}

@router.get("/auth")
async def protected_route(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Check access via access token
    :param current_user: User credentials
    :type current_user: dict
    :return: User dict
    :rtype: dict
    """
    return {"message": f"Beware, {current_user['username']}. You are logged in!"}
