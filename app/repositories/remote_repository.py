"""Repository layer that communicates with the TodayPickup API."""
from typing import Any, Dict
import httpx

class TodayPickupRepository:
    """HTTP repository using httpx to call external APIs."""

    def __init__(self, base_url: str = "https://admin.todaypickup.com"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def request(self, method: str, path: str, headers: Dict[str, str], json: Any = None) -> httpx.Response:
        """Make an HTTP request."""
        response = await self.client.request(method, path, headers=headers, json=json)
        response.raise_for_status()
        return response

    async def close(self) -> None:
        await self.client.aclose()
