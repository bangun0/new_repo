"""
대리점(Agency) API Repository
대리점 관련 API 호출을 담당합니다.
"""
from typing import Any, Dict, List, Optional
import logging

from app.repositories.base import BaseRepository
from app.models.base import AuthInfo
from app.schemas.agency import (
    TokenGenerationRequest,
    TokenValidationRequest,
    DeliveryAssignmentRequest,
    DeliveryInfoRequest
)

logger = logging.getLogger(__name__)


class AgencyRepository(BaseRepository):
    """
    대리점 API Repository 클래스
    대리점 관련 API 엔드포인트와의 통신을 담당합니다.
    """
    
    def __init__(self):
        """AgencyRepository 초기화"""
        super().__init__()
        self.agency_prefix = f"{self.api_prefix}/agency"
        
    async def health_check(self) -> bool:
        """
        Repository 상태 확인
        
        Returns:
            bool: 상태 확인 결과
        """
        try:
            # 간단한 GET 요청으로 API 서버 상태 확인
            response = await self.http_client.get("/")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Agency repository health check failed: {e}")
            return False
    
    async def generate_token(self, request: TokenGenerationRequest) -> Dict[str, Any]:
        """
        인증 토큰을 생성합니다.
        
        Args:
            request: 토큰 생성 요청 데이터
            
        Returns:
            Dict[str, Any]: 토큰 생성 응답 데이터
        """
        endpoint = f"{self.agency_prefix}/auth/token"
        
        response = await self.http_client.post(
            endpoint=endpoint,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def validate_token(self, request: TokenValidationRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        토큰 유효성을 검증합니다.
        
        Args:
            request: 토큰 검증 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 토큰 검증 응답 데이터
        """
        endpoint = f"{self.agency_prefix}/auth"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def assign_delivery(self, request: DeliveryAssignmentRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송을 배정합니다.
        
        Args:
            request: 배송 배정 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 배정 응답 데이터
        """
        endpoint = f"{self.agency_prefix}/delivery"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.put(
            endpoint=endpoint,
            headers=headers,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def get_delivery_list(self, delivery_date: str, auth_info: AuthInfo, **kwargs) -> Dict[str, Any]:
        """
        배송 목록을 조회합니다.
        
        Args:
            delivery_date: 배송일자 (YYYY-MM-DD)
            auth_info: 인증 정보
            **kwargs: 추가 쿼리 파라미터
            
        Returns:
            Dict[str, Any]: 배송 목록 응답 데이터
        """
        endpoint = f"{self.agency_prefix}/delivery/list/{delivery_date}"
        headers = self._build_headers(auth_info)
        
        # 쿼리 파라미터 구성
        params = {}
        if kwargs.get('status'):
            params['status'] = kwargs['status']
        if kwargs.get('page'):
            params['page'] = kwargs['page']
        if kwargs.get('size'):
            params['size'] = kwargs['size']
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            params=params if params else None
        )
        
        return await self._handle_response(response)
    
    async def get_postal_code_info(self, zipcode: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        우편번호 정보를 조회합니다.
        
        Args:
            zipcode: 우편번호
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 우편번호 정보 응답 데이터
        """
        endpoint = f"{self.agency_prefix}/postalcode/{zipcode}"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.get(
            endpoint=endpoint,
            headers=headers
        )
        
        return await self._handle_response(response)