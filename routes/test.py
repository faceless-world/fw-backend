from fastapi import APIRouter, Depends
from modules.api.auth import get_current_user

router = APIRouter(
    prefix="/test",
    tags=["test"]
)

@router.get("")
async def test():
    return {"status": "ok"}

@router.get("/auth")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Beware, {current_user['username']}. You are logged in!"}
