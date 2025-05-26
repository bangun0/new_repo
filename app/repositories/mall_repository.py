"""
쇼핑몰(Mall) API Repository
쇼핑몰 관련 API 호출을 담당합니다.
"""
from typing import Any, Dict, List, Optional
import logging

from app.repositories.base import BaseRepository
from app.models.base import AuthInfo
from app.schemas.mall import (
    SingleDeliveryRegisterRequest,
    MultipleDeliveryRegisterRequest,
    DeliveryAvailabilityRequest,
    DeliveryCancelRequest,
    DeliveryReturnRequest
)

logger = logging.getLogger(__name__)


class MallRepository(BaseRepository):
    """
    쇼핑몰 API Repository 클래스
    쇼핑몰 관련 API 엔드포인트와의 통신을 담당합니다.
    """
    
    def __init__(self):
        """MallRepository 초기화"""
        super().__init__()
        self.mall_prefix = f"{self.api_prefix}/mall"
        
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
            logger.error(f"Mall repository health check failed: {e}")
            return False
    
    async def register_single_delivery(self, request: SingleDeliveryRegisterRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        단일 배송을 등록합니다.
        
        Args:
            request: 단일 배송 등록 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 등록 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/deliveryRegister"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def register_multiple_deliveries(self, request: MultipleDeliveryRegisterRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        다중 배송을 등록합니다.
        
        Args:
            request: 다중 배송 등록 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 다중 배송 등록 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/deliveryListRegister"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def track_delivery(self, invoice_number: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송을 추적합니다.
        
        Args:
            invoice_number: 송장번호
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 추적 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/delivery/{invoice_number}"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.get(
            endpoint=endpoint,
            headers=headers
        )
        
        return await self._handle_response(response)
    
    async def check_delivery_availability(self, request: DeliveryAvailabilityRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송 가능 여부를 확인합니다.
        
        Args:
            request: 배송 가능 여부 확인 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 가능 여부 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/possibleDelivery"
        headers = self._build_headers(auth_info)
        
        params = {
            "zipcode": request.zipcode,
            "deliveryDate": request.delivery_date
        }
        
        response = await self.http_client.get(
            endpoint=endpoint,
            headers=headers,
            params=params
        )
        
        return await self._handle_response(response)
    
    async def cancel_delivery(self, request: DeliveryCancelRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송을 취소합니다.
        
        Args:
            request: 배송 취소 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 취소 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/delivery/{request.invoice_number}/cancel"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            json_data={"cancel_reason": request.cancel_reason}
        )
        
        return await self._handle_response(response)
    
    async def request_return_delivery(self, request: DeliveryReturnRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        반품 배송을 요청합니다.
        
        Args:
            request: 반품 배송 요청 데이터
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 반품 배송 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/delivery/return"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.post(
            endpoint=endpoint,
            headers=headers,
            json_data=request.dict()
        )
        
        return await self._handle_response(response)
    
    async def get_delivery_history(self, invoice_number: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송 이력을 조회합니다.
        
        Args:
            invoice_number: 송장번호
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 이력 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/delivery/{invoice_number}/history"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.get(
            endpoint=endpoint,
            headers=headers
        )
        
        return await self._handle_response(response)
    
    async def update_delivery_status(self, invoice_number: str, status: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송 상태를 업데이트합니다.
        
        Args:
            invoice_number: 송장번호
            status: 업데이트할 상태
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 상태 업데이트 응답 데이터
        """
        endpoint = f"{self.mall_prefix}/delivery/{invoice_number}/status"
        headers = self._build_headers(auth_info)
        
        response = await self.http_client.put(
            endpoint=endpoint,
            headers=headers,
            json_data={"status": status}
        )
        
        return await self._handle_response(response)