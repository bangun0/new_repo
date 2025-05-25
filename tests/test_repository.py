import pytest
import httpx
from app.repositories.remote_repository import TodayPickupRepository


@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio("asyncio")
async def test_request_success(monkeypatch):
    async def mock_send(request, *args, **kwargs):
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(mock_send)
    repo = TodayPickupRepository()
    repo.client = httpx.AsyncClient(transport=transport, base_url=repo.base_url)

    resp = await repo.request("GET", "/some", headers={})
    assert resp.json() == {"ok": True}
    await repo.close()
