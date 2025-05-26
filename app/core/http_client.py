"""
HTTP 클라이언트 유틸리티
TodayPickup API와의 통신을 담당합니다.
"""
import logging
from typing import Any, Dict, Optional
import httpx
from httpx import Response

from app.core.config import settings

logger = logging.getLogger(__name__)


class HTTPClient:
    """
    HTTP 클라이언트 클래스
    TodayPickup API와의 HTTP 통신을 처리합니다.
    """
    
    def __init__(self):
        """HTTP 클라이언트 초기화"""
        self.base_url = settings.TODAYPICKUP_BASE_URL
        self.timeout = settings.HTTP_TIMEOUT
        
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        HTTP 요청을 실행합니다.
        
        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트 경로
            headers: 요청 헤더
            params: 쿼리 파라미터
            json_data: JSON 요청 바디
            
        Returns:
            httpx.Response: HTTP 응답 객체
            
        Raises:
            httpx.HTTPError: HTTP 요청 실패 시
        """
        url = f"{self.base_url}{endpoint}"
        
        # 기본 헤더 설정
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if headers:
            default_headers.update(headers)
            
        logger.info(f"Making {method} request to {url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=default_headers,
                params=params,
                json=json_data
            )
            
        logger.info(f"Response status: {response.status_code}")
        return response
        
    async def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        GET 요청을 실행합니다.
        
        Args:
            endpoint: API 엔드포인트 경로
            headers: 요청 헤더
            params: 쿼리 파라미터
            
        Returns:
            httpx.Response: HTTP 응답 객체
        """
        return await self._make_request("GET", endpoint, headers, params)
        
    async def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        POST 요청을 실행합니다.
        
        Args:
            endpoint: API 엔드포인트 경로
            headers: 요청 헤더
            json_data: JSON 요청 바디
            
        Returns:
            httpx.Response: HTTP 응답 객체
        """
        return await self._make_request("POST", endpoint, headers, json_data=json_data)
        
    async def put(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Response:
        """
        PUT 요청을 실행합니다.
        
        Args:
            endpoint: API 엔드포인트 경로
            headers: 요청 헤더
            json_data: JSON 요청 바디
            
        Returns:
            httpx.Response: HTTP 응답 객체
        """
        return await self._make_request("PUT", endpoint, headers, json_data=json_data)
        
    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """
        DELETE 요청을 실행합니다.
        
        Args:
            endpoint: API 엔드포인트 경로
            headers: 요청 헤더
            
        Returns:
            httpx.Response: HTTP 응답 객체
        """
        return await self._make_request("DELETE", endpoint, headers)


# 전역 HTTP 클라이언트 인스턴스
http_client = HTTPClient()