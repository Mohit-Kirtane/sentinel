from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from app.auth.dependencies import get_current_username
from app.auth.security import COOKIE_NAME, create_access_token, verify_password
from app.core.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginRequest, response: Response) -> dict:
    settings = get_settings()
    if payload.username != settings.demo_username or not settings.demo_password_hash:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not verify_password(payload.password, settings.demo_password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    response.set_cookie(
        key=COOKIE_NAME,
        value=create_access_token(settings.demo_username),
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
    )
    return {"username": settings.demo_username}


@router.post("/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me")
def me(username: str = Depends(get_current_username)) -> dict:
    return {"username": username}
