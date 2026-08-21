import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.models import User
from app.db.session import get_db
from app.main import app

pytestmark = pytest.mark.asyncio


@pytest.fixture
def db_session():
    # StaticPool: a plain sqlite:///:memory: engine opens a fresh, separate
    # in-memory database on every new connection - StaticPool pins the whole
    # engine to one connection so the schema/data created below actually
    # persists across the session's queries.
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    User.__table__.create(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    transport = ASGITransport(app=app)
    yield AsyncClient(transport=transport, base_url="http://test")
    app.dependency_overrides.clear()


async def test_register_creates_an_account_and_signs_in(client):
    res = await client.post(
        "/api/auth/register", json={"email": "new@example.com", "password": "correct-password"}
    )
    assert res.status_code == 200
    assert res.json()["email"] == "new@example.com"
    assert "access_token" in res.cookies

    me_res = await client.get("/api/auth/me")
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "new@example.com"


async def test_register_rejects_an_invalid_email(client):
    res = await client.post(
        "/api/auth/register", json={"email": "not-an-email", "password": "correct-password"}
    )
    assert res.status_code == 400


async def test_register_rejects_a_short_password(client):
    res = await client.post("/api/auth/register", json={"email": "new@example.com", "password": "short"})
    assert res.status_code == 400


async def test_register_rejects_a_duplicate_email(client):
    await client.post("/api/auth/register", json={"email": "dup@example.com", "password": "correct-password"})
    res = await client.post(
        "/api/auth/register", json={"email": "dup@example.com", "password": "another-password"}
    )
    assert res.status_code == 409


async def test_me_without_a_session_is_401(client):
    res = await client.get("/api/auth/me")
    assert res.status_code == 401


async def test_login_with_wrong_password_is_401(client):
    await client.post("/api/auth/register", json={"email": "user@example.com", "password": "correct-password"})
    res = await client.post("/api/auth/login", json={"email": "user@example.com", "password": "wrong"})
    assert res.status_code == 401


async def test_login_with_correct_credentials_sets_a_cookie_and_grants_access(client):
    await client.post("/api/auth/register", json={"email": "user@example.com", "password": "correct-password"})
    await client.post("/api/auth/logout")

    login_res = await client.post(
        "/api/auth/login", json={"email": "user@example.com", "password": "correct-password"}
    )
    assert login_res.status_code == 200
    assert "access_token" in login_res.cookies

    me_res = await client.get("/api/auth/me")
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "user@example.com"


async def test_logout_clears_the_session(client):
    await client.post("/api/auth/register", json={"email": "user@example.com", "password": "correct-password"})
    await client.post("/api/auth/logout")

    me_res = await client.get("/api/auth/me")
    assert me_res.status_code == 401


async def test_videos_endpoint_requires_authentication(client):
    res = await client.get("/api/videos")
    assert res.status_code == 401
