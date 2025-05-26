"""
대리점(Agency) Service
대리점 관련 비즈니스 로직을 담당합니다.
"""
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from app.services.base import BaseService
from app.repositories.agency_repository import AgencyRepository
from app.models.base import AuthInfo
from app.schemas.agency import (
    TokenGenerationRequest,
    TokenValidationRequest,
    DeliveryAssignmentRequest,
    DeliveryInfoRequest
)

logger = logging.getLogger(__name__)


class AgencyService(BaseService):
    """
    대리점 Service 클래스
    대리점 관련 비즈니스 로직을 처리합니다.
    """
    
    def __init__(self):
        """AgencyService 초기화"""
        super().__init__()
        self.repository = AgencyRepository()
        
    async def health_check(self) -> Dict[str, Any]:
        """
        서비스 상태 확인
        
        Returns:
            Dict[str, Any]: 상태 확인 결과
        """
        try:
            is_healthy = await self.repository.health_check()
            return self._create_success_response(
                {"is_healthy": is_healthy},
                "Agency service health check completed"
            )
        except Exception as e:
            return self._handle_service_error(e, "Agency service health check")
    
    async def generate_authentication_token(self, agency_id: str, api_key: str) -> Dict[str, Any]:
        """
        인증 토큰을 생성합니다.
        
        Args:
            agency_id: 대리점 ID
            api_key: API 키
            
        Returns:
            Dict[str, Any]: 토큰 생성 결과
        """
        try:
            # 입력값 검증
            if not agency_id or not api_key:
                return {
                    "success": False,
                    "message": "Agency ID and API key are required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            request = TokenGenerationRequest(agency_id=agency_id, api_key=api_key)
            response_data = await self.repository.generate_token(request)
            
            logger.info(f"Token generated successfully for agency: {agency_id}")
            return self._create_success_response(
                response_data,
                "Authentication token generated successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Token generation")
    
    async def validate_authentication_token(self, token: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        토큰 유효성을 검증합니다.
        
        Args:
            token: 검증할 토큰
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 토큰 검증 결과
        """
        try:
            # 인증 정보 검증
            if not self._validate_auth_info(auth_info):
                return {
                    "success": False,
                    "message": "Invalid authentication information",
                    "error_code": "INVALID_AUTH",
                    "data": None
                }
            
            # 토큰 검증
            if not token:
                return {
                    "success": False,
                    "message": "Token is required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            request = TokenValidationRequest(token=token)
            response_data = await self.repository.validate_token(request, auth_info)
            
            logger.info(f"Token validation completed for agency: {auth_info.agency_id}")
            return self._create_success_response(
                response_data,
                "Token validation completed"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Token validation")
    
    async def assign_delivery_to_driver(
        self,
        invoice_number: str,
        auth_info: AuthInfo,
        driver_id: Optional[str] = None,
        driver_name: Optional[str] = None,
        driver_phone: Optional[str] = None,
        estimated_delivery_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        배송을 기사에게 배정합니다.
        
        Args:
            invoice_number: 송장번호
            auth_info: 인증 정보
            driver_id: 기사 ID
            driver_name: 기사 이름
            driver_phone: 기사 전화번호
            estimated_delivery_time: 예상 배송 시간
            
        Returns:
            Dict[str, Any]: 배송 배정 결과
        """
        try:
            # 인증 정보 검증
            if not self._validate_auth_info(auth_info):
                return {
                    "success": False,
                    "message": "Invalid authentication information",
                    "error_code": "INVALID_AUTH",
                    "data": None
                }
            
            # 송장번호 검증
            if not invoice_number:
                return {
                    "success": False,
                    "message": "Invoice number is required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            request = DeliveryAssignmentRequest(
                invoice_number=invoice_number,
                driver_id=driver_id,
                driver_name=driver_name,
                driver_phone=driver_phone,
                estimated_delivery_time=estimated_delivery_time
            )
            
            response_data = await self.repository.assign_delivery(request, auth_info)
            
            logger.info(f"Delivery assigned successfully: {invoice_number}")
            return self._create_success_response(
                response_data,
                "Delivery assigned successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Delivery assignment")
    
    async def get_delivery_information_list(
        self,
        delivery_date: str,
        auth_info: AuthInfo,
        status: Optional[str] = None,
        page: int = 1,
        size: int = 10
    ) -> Dict[str, Any]:
        """
        배송 정보 목록을 조회합니다.
        
        Args:
            delivery_date: 배송일자 (YYYY-MM-DD)
            auth_info: 인증 정보
            status: 배송 상태 필터
            page: 페이지 번호
            size: 페이지 크기
            
        Returns:
            Dict[str, Any]: 배송 정보 목록
        """
        try:
            # 인증 정보 검증
            if not self._validate_auth_info(auth_info):
                return {
                    "success": False,
                    "message": "Invalid authentication information",
                    "error_code": "INVALID_AUTH",
                    "data": None
                }
            
            # 배송일자 형식 검증
            if not delivery_date:
                return {
                    "success": False,
                    "message": "Delivery date is required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            try:
                datetime.strptime(delivery_date, '%Y-%m-%d')
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid delivery date format. Use YYYY-MM-DD",
                    "error_code": "INVALID_DATE_FORMAT",
                    "data": None
                }
            
            # 페이지네이션 검증
            if page < 1 or size < 1:
                return {
                    "success": False,
                    "message": "Page and size must be positive integers",
                    "error_code": "INVALID_PAGINATION",
                    "data": None
                }
            
            response_data = await self.repository.get_delivery_list(
                delivery_date=delivery_date,
                auth_info=auth_info,
                status=status,
                page=page,
                size=size
            )
            
            logger.info(f"Delivery information retrieved for date: {delivery_date}")
            return self._create_success_response(
                response_data,
                "Delivery information retrieved successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Delivery information retrieval")
    
    async def get_postal_code_information(self, zipcode: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        우편번호 정보를 조회합니다.
        
        Args:
            zipcode: 우편번호
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 우편번호 정보
        """
        try:
            # 인증 정보 검증
            if not self._validate_auth_info(auth_info):
                return {
                    "success": False,
                    "message": "Invalid authentication information",
                    "error_code": "INVALID_AUTH",
                    "data": None
                }
            
            # 우편번호 검증
            if not zipcode or len(zipcode.strip()) == 0:
                return {
                    "success": False,
                    "message": "Zipcode is required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            response_data = await self.repository.get_postal_code_info(zipcode, auth_info)
            
            logger.info(f"Postal code information retrieved: {zipcode}")
            return self._create_success_response(
                response_data,
                "Postal code information retrieved successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Postal code information retrieval")