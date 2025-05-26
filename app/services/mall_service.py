"""
쇼핑몰(Mall) Service
쇼핑몰 관련 비즈니스 로직을 담당합니다.
"""
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

from app.services.base import BaseService
from app.repositories.mall_repository import MallRepository
from app.models.base import AuthInfo
from app.schemas.mall import (
    SingleDeliveryRegisterRequest,
    MultipleDeliveryRegisterRequest,
    DeliveryAvailabilityRequest,
    DeliveryCancelRequest,
    DeliveryReturnRequest
)

logger = logging.getLogger(__name__)


class MallService(BaseService):
    """
    쇼핑몰 Service 클래스
    쇼핑몰 관련 비즈니스 로직을 처리합니다.
    """
    
    def __init__(self):
        """MallService 초기화"""
        super().__init__()
        self.repository = MallRepository()
        
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
                "Mall service health check completed"
            )
        except Exception as e:
            return self._handle_service_error(e, "Mall service health check")
    
    async def register_single_delivery(self, request: SingleDeliveryRegisterRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        단일 배송을 등록합니다.
        
        Args:
            request: 단일 배송 등록 요청
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 등록 결과
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
            
            # 요청 데이터 검증
            validation_result = self._validate_delivery_request(request)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "message": validation_result["message"],
                    "error_code": "INVALID_REQUEST",
                    "data": None
                }
            
            response_data = await self.repository.register_single_delivery(request, auth_info)
            
            logger.info(f"Single delivery registered successfully: {request.mall_order_number}")
            return self._create_success_response(
                response_data,
                "Single delivery registered successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Single delivery registration")
    
    async def register_multiple_deliveries(self, request: MultipleDeliveryRegisterRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        다중 배송을 등록합니다.
        
        Args:
            request: 다중 배송 등록 요청
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 다중 배송 등록 결과
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
            
            # 배송 목록 검증
            if not request.deliveries or len(request.deliveries) == 0:
                return {
                    "success": False,
                    "message": "At least one delivery is required",
                    "error_code": "EMPTY_DELIVERY_LIST",
                    "data": None
                }
            
            if len(request.deliveries) > 100:
                return {
                    "success": False,
                    "message": "Maximum 100 deliveries allowed per request",
                    "error_code": "TOO_MANY_DELIVERIES",
                    "data": None
                }
            
            # 각 배송 요청 검증
            for idx, delivery in enumerate(request.deliveries):
                validation_result = self._validate_delivery_request(delivery)
                if not validation_result["is_valid"]:
                    return {
                        "success": False,
                        "message": f"Invalid delivery at index {idx}: {validation_result['message']}",
                        "error_code": "INVALID_REQUEST",
                        "data": None
                    }
            
            response_data = await self.repository.register_multiple_deliveries(request, auth_info)
            
            logger.info(f"Multiple deliveries registered: {len(request.deliveries)} deliveries")
            return self._create_success_response(
                response_data,
                "Multiple deliveries registered successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Multiple delivery registration")
    
    async def track_delivery_status(self, invoice_number: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송 상태를 추적합니다.
        
        Args:
            invoice_number: 송장번호
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 추적 결과
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
            if not invoice_number or len(invoice_number.strip()) == 0:
                return {
                    "success": False,
                    "message": "Invoice number is required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            response_data = await self.repository.track_delivery(invoice_number, auth_info)
            
            logger.info(f"Delivery tracking completed: {invoice_number}")
            return self._create_success_response(
                response_data,
                "Delivery tracking completed successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Delivery tracking")
    
    async def check_delivery_availability(self, zipcode: str, delivery_date: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송 가능 여부를 확인합니다.
        
        Args:
            zipcode: 우편번호
            delivery_date: 배송 예정일
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 가능 여부 확인 결과
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
            
            # 입력값 검증
            if not zipcode or not delivery_date:
                return {
                    "success": False,
                    "message": "Zipcode and delivery date are required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            # 날짜 형식 검증
            try:
                datetime.strptime(delivery_date, '%Y-%m-%d')
            except ValueError:
                return {
                    "success": False,
                    "message": "Invalid delivery date format. Use YYYY-MM-DD",
                    "error_code": "INVALID_DATE_FORMAT",
                    "data": None
                }
            
            request = DeliveryAvailabilityRequest(zipcode=zipcode, delivery_date=delivery_date)
            response_data = await self.repository.check_delivery_availability(request, auth_info)
            
            logger.info(f"Delivery availability checked: {zipcode}, {delivery_date}")
            return self._create_success_response(
                response_data,
                "Delivery availability checked successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Delivery availability check")
    
    async def cancel_delivery(self, invoice_number: str, cancel_reason: str, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        배송을 취소합니다.
        
        Args:
            invoice_number: 송장번호
            cancel_reason: 취소 사유
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 배송 취소 결과
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
            
            # 입력값 검증
            if not invoice_number or not cancel_reason:
                return {
                    "success": False,
                    "message": "Invoice number and cancel reason are required",
                    "error_code": "INVALID_INPUT",
                    "data": None
                }
            
            request = DeliveryCancelRequest(invoice_number=invoice_number, cancel_reason=cancel_reason)
            response_data = await self.repository.cancel_delivery(request, auth_info)
            
            logger.info(f"Delivery cancelled successfully: {invoice_number}")
            return self._create_success_response(
                response_data,
                "Delivery cancelled successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Delivery cancellation")
    
    async def request_return_delivery(self, request: DeliveryReturnRequest, auth_info: AuthInfo) -> Dict[str, Any]:
        """
        반품 배송을 요청합니다.
        
        Args:
            request: 반품 배송 요청
            auth_info: 인증 정보
            
        Returns:
            Dict[str, Any]: 반품 배송 요청 결과
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
            
            # 반품 요청 검증
            validation_result = self._validate_return_request(request)
            if not validation_result["is_valid"]:
                return {
                    "success": False,
                    "message": validation_result["message"],
                    "error_code": "INVALID_REQUEST",
                    "data": None
                }
            
            response_data = await self.repository.request_return_delivery(request, auth_info)
            
            logger.info(f"Return delivery requested: {request.original_invoice_number}")
            return self._create_success_response(
                response_data,
                "Return delivery requested successfully"
            )
            
        except Exception as e:
            return self._handle_service_error(e, "Return delivery request")
    
    def _validate_delivery_request(self, request: SingleDeliveryRegisterRequest) -> Dict[str, Any]:
        """
        배송 등록 요청을 검증합니다.
        
        Args:
            request: 배송 등록 요청
            
        Returns:
            Dict[str, Any]: 검증 결과
        """
        # 필수 필드 검증
        if not request.mall_order_number:
            return {"is_valid": False, "message": "Mall order number is required"}
        
        if not request.delivery_date:
            return {"is_valid": False, "message": "Delivery date is required"}
        
        if not request.address:
            return {"is_valid": False, "message": "Address information is required"}
        
        if not request.items or len(request.items) == 0:
            return {"is_valid": False, "message": "At least one item is required"}
        
        # 주소 정보 검증
        address = request.address
        if not address.zipcode or not address.address or not address.receiver_name or not address.receiver_phone:
            return {"is_valid": False, "message": "Complete address information is required"}
        
        # 상품 정보 검증
        for item in request.items:
            if not item.item_name or item.quantity <= 0 or item.price < 0:
                return {"is_valid": False, "message": "Invalid item information"}
        
        return {"is_valid": True, "message": "Valid request"}
    
    def _validate_return_request(self, request: DeliveryReturnRequest) -> Dict[str, Any]:
        """
        반품 요청을 검증합니다.
        
        Args:
            request: 반품 요청
            
        Returns:
            Dict[str, Any]: 검증 결과
        """
        # 필수 필드 검증
        if not request.original_invoice_number:
            return {"is_valid": False, "message": "Original invoice number is required"}
        
        if not request.return_reason:
            return {"is_valid": False, "message": "Return reason is required"}
        
        if not request.return_address:
            return {"is_valid": False, "message": "Return address is required"}
        
        if not request.return_items or len(request.return_items) == 0:
            return {"is_valid": False, "message": "At least one return item is required"}
        
        # 반품 주소 검증
        address = request.return_address
        if not address.zipcode or not address.address or not address.receiver_name or not address.receiver_phone:
            return {"is_valid": False, "message": "Complete return address information is required"}
        
        # 반품 상품 검증
        for item in request.return_items:
            if not item.item_name or item.quantity <= 0:
                return {"is_valid": False, "message": "Invalid return item information"}
        
        return {"is_valid": True, "message": "Valid return request"}