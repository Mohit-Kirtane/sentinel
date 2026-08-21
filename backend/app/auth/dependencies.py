from fastapi import HTTPException, Request

from app.auth.security import COOKIE_NAME, decode_access_token
from app.core.config import get_settings


def get_current_username(request: Request) -> str:
    token = request.cookies.get(COOKIE_NAME)
    username = decode_access_token(token) if token else None
    if not username or username != get_settings().demo_username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username
