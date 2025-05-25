import pytest
import httpx
from app.services.agency_service import AgencyService
from app.repositories.remote_repository import TodayPickupRepository
from app.schemas import models


@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio("asyncio")
async def test_auth(monkeypatch):
    async def mock_send(request, *args, **kwargs):
        assert request.url.path == "/api/agency/auth"
        return httpx.Response(200, json={"token": "abc"})

    transport = httpx.MockTransport(mock_send)
    repo = TodayPickupRepository()
    repo.client = httpx.AsyncClient(transport=transport, base_url=repo.base_url)
    service = AgencyService(repo)

    result = await service.auth({})
    assert result == {"token": "abc"}
    await repo.close()
