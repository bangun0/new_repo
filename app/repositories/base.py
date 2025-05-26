"""
기본 Repository 클래스
모든 Repository의 베이스 클래스를 정의합니다.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from httpx import Response

from app.core.http_client import http_client
from app.models.base import AuthInfo


class BaseRepository(ABC):
    """
    기본 Repository 클래스
    TodayPickup API와의 데이터 액세스를 담당하는 베이스 클래스입니다.
    """
    
    def __init__(self):
        """Repository 초기화"""
        self.http_client = http_client
        self.api_prefix = "/api"
        
    def _build_headers(self, auth_info: AuthInfo, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        요청 헤더를 구성합니다.
        
        Args:
            auth_info: 인증 정보
            additional_headers: 추가 헤더
            
        Returns:
            Dict[str, str]: 구성된 헤더 딕셔너리
        """
        headers = auth_info.to_headers()
        
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
        
    async def _handle_response(self, response: Response) -> Dict[str, Any]:
        """
        HTTP 응답을 처리합니다.
        
        Args:
            response: HTTP 응답 객체
            
        Returns:
            Dict[str, Any]: 처리된 응답 데이터
            
        Raises:
            Exception: API 오류 발생 시
        """
        try:
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # 응답에서 에러 정보 추출
            error_data = {}
            try:
                error_data = response.json()
            except:
                error_data = {"message": str(e), "status_code": response.status_code}
                
            raise Exception(f"API Error: {error_data}")
            
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Repository 상태 확인
        
        Returns:
            bool: 상태 확인 결과
        """
        pass