"""
기본 Service 클래스
모든 Service의 베이스 클래스를 정의합니다.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from app.models.base import AuthInfo
from app.core.config import settings

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    기본 Service 클래스
    비즈니스 로직을 담당하는 베이스 클래스입니다.
    """
    
    def __init__(self):
        """Service 초기화"""
        self.settings = settings
        
    def _validate_auth_info(self, auth_info: AuthInfo) -> bool:
        """
        인증 정보의 유효성을 검증합니다.
        
        Args:
            auth_info: 인증 정보
            
        Returns:
            bool: 유효성 검증 결과
        """
        if not auth_info or not auth_info.agency_id or not auth_info.auth_token:
            logger.error("Invalid auth info: missing agency_id or auth_token")
            return False
            
        if len(auth_info.agency_id.strip()) == 0:
            logger.error("Invalid auth info: empty agency_id")
            return False
            
        if len(auth_info.auth_token.strip()) == 0:
            logger.error("Invalid auth info: empty auth_token")
            return False
            
        return True
    
    def _create_default_auth_info(self) -> Optional[AuthInfo]:
        """
        기본 인증 정보를 생성합니다.
        
        Returns:
            Optional[AuthInfo]: 기본 인증 정보 (설정되지 않은 경우 None)
        """
        if self.settings.DEFAULT_AGENCY_ID and self.settings.DEFAULT_AUTH_TOKEN:
            return AuthInfo(
                agency_id=self.settings.DEFAULT_AGENCY_ID,
                auth_token=self.settings.DEFAULT_AUTH_TOKEN
            )
        return None
    
    def _handle_service_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """
        서비스 에러를 처리합니다.
        
        Args:
            error: 발생한 에러
            operation: 수행 중이던 작업명
            
        Returns:
            Dict[str, Any]: 에러 응답 데이터
        """
        error_message = f"{operation} failed: {str(error)}"
        logger.error(error_message)
        
        return {
            "success": False,
            "message": error_message,
            "error_code": "SERVICE_ERROR",
            "data": None
        }
    
    def _create_success_response(self, data: Any, message: str = "Operation successful") -> Dict[str, Any]:
        """
        성공 응답을 생성합니다.
        
        Args:
            data: 응답 데이터
            message: 성공 메시지
            
        Returns:
            Dict[str, Any]: 성공 응답 데이터
        """
        return {
            "success": True,
            "message": message,
            "data": data,
            "error_code": None
        }
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        서비스 상태 확인
        
        Returns:
            Dict[str, Any]: 상태 확인 결과
        """
        pass