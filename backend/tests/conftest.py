import pytest
from httpx import ASGITransport, AsyncClient

from app.auth.dependencies import get_current_user
from app.api.routes.videos import get_chat_fn, get_embed_fn, get_repo
from app.db.models import User
from app.main import app

from .fakes import FakeRepository


@pytest.fixture
def fake_repo():
    return FakeRepository()


@pytest.fixture
def api_client(fake_repo):
    app.dependency_overrides[get_repo] = lambda: fake_repo
    app.dependency_overrides[get_embed_fn] = lambda: (lambda text: [1.0, 0.0])
    app.dependency_overrides[get_chat_fn] = lambda: (lambda messages: "stub answer")
    app.dependency_overrides[get_current_user] = lambda: User(id="user-1", email="user@example.com")

    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    app.dependency_overrides.clear()
