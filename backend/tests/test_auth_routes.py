import pytest
from httpx import ASGITransport, AsyncClient

from app.auth.security import hash_password
from app.core.config import get_settings
from app.main import app

pytestmark = pytest.mark.asyncio


@pytest.fixture
def unauthenticated_client(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "demo_username", "demo")
    monkeypatch.setattr(settings, "demo_password_hash", hash_password("correct-password"))
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


async def test_me_without_a_session_is_401(unauthenticated_client):
    res = await unauthenticated_client.get("/api/auth/me")
    assert res.status_code == 401


async def test_login_with_wrong_password_is_401(unauthenticated_client):
    res = await unauthenticated_client.post(
        "/api/auth/login", json={"username": "demo", "password": "wrong"}
    )
    assert res.status_code == 401


async def test_login_with_correct_credentials_sets_a_cookie_and_grants_access(unauthenticated_client):
    login_res = await unauthenticated_client.post(
        "/api/auth/login", json={"username": "demo", "password": "correct-password"}
    )
    assert login_res.status_code == 200
    assert "access_token" in login_res.cookies

    me_res = await unauthenticated_client.get("/api/auth/me")
    assert me_res.status_code == 200
    assert me_res.json() == {"username": "demo"}


async def test_logout_clears_the_session(unauthenticated_client):
    await unauthenticated_client.post(
        "/api/auth/login", json={"username": "demo", "password": "correct-password"}
    )
    await unauthenticated_client.post("/api/auth/logout")

    me_res = await unauthenticated_client.get("/api/auth/me")
    assert me_res.status_code == 401


async def test_videos_endpoint_requires_authentication(unauthenticated_client):
    res = await unauthenticated_client.get("/api/videos")
    assert res.status_code == 401
