"""
This module provides a base class for repositories that interact with external APIs.
It includes common HTTP request logic and client lifecycle management using httpx.
"""
import httpx
from typing import Optional, Dict, Any

class BaseRepository:
    """
    A base repository class for making asynchronous HTTP requests to an external API.

    This class initializes an `httpx.AsyncClient` for making requests and provides
    a common interface for request execution and client lifecycle management.
    The base URL for the API is configurable.
    """
    def __init__(self, base_url: str = "https://admin.todaypickup.com"):
        """
        Initializes the BaseRepository.

        Args:
            base_url: The base URL for the API. Defaults to the Kakao T TodayPickup admin URL.
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        """
        Closes the underlying httpx.AsyncClient.
        This should be called during application shutdown to release resources.
        """
        await self.client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Makes an asynchronous HTTP request to the specified endpoint.

        This method handles the construction of the request, sending it,
        and basic error handling for HTTP status codes.

        Args:
            method: HTTP method (e.g., "GET", "POST", "PUT").
            endpoint: API endpoint path (relative to the base_url).
            data: JSON serializable data for the request body (for methods like POST, PUT).
            params: Query parameters to be appended to the URL.
            headers: Custom HTTP headers for the request.

        Returns:
            The httpx.Response object containing the server's response.
        
        Raises:
            httpx.HTTPStatusError: For 4xx client errors or 5xx server errors.
            httpx.RequestError: For other request-related issues (e.g., network problems).
        """
        try:
            response = await self.client.request(
                method,
                endpoint,
                json=data,
                params=params,
                headers=headers,
            )
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response
        except httpx.HTTPStatusError as e:
            # Log error or handle specific statuses if needed
            # For now, just re-raising after printing.
            print(f"HTTP error occurred: {e.response.status_code} for URL {e.request.url}")
            raise
        except httpx.RequestError as e:
            # Handle other request errors (e.g., network issues, timeouts)
            print(f"Request error occurred for URL {e.request.url}: {e}")
            raise
