"""
쇼핑몰(Mall) Controller
쇼핑몰 관련 FastAPI 엔드포인트를 정의합니다.
"""
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Header, Query, Depends
import logging

from app.services.mall_service import MallService
from app.models.base import AuthInfo
from app.schemas.mall import (
    SingleDeliveryRegisterRequest,
    MultipleDeliveryRegisterRequest,
    DeliveryRegisterResponse,
    MultipleDeliveryRegisterResponse,
    DeliveryTrackingResponse,
    DeliveryAvailabilityResponse,
    DeliveryCancelRequest,
    DeliveryCancelResponse,
    DeliveryReturnRequest,
    DeliveryReturnResponse
)

logger = logging.getLogger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

# MallService 인스턴스
mall_service = MallService()


def get_auth_info(
    authorization: str = Header(..., description="인증 토큰"),
    agency_id: str = Header(..., alias="AgencyId", description="대리점 ID")
) -> AuthInfo:
    """
    헤더에서 인증 정보를 추출합니다.
    
    Args:
        authorization: 인증 토큰
        agency_id: 대리점 ID
        
    Returns:
        AuthInfo: 인증 정보 객체
    """
    return AuthInfo(agency_id=agency_id, auth_token=authorization)


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    쇼핑몰 서비스 상태 확인
    
    Returns:
        Dict[str, Any]: 서비스 상태 정보
    """
    try:
        result = await mall_service.health_check()
        return result
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service health check failed")


@router.post("/deliveryRegister", response_model=DeliveryRegisterResponse)
async def register_single_delivery(
    request: SingleDeliveryRegisterRequest,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryRegisterResponse:
    """
    단일 배송을 등록합니다.
    
    Args:
        request: 단일 배송 등록 요청 데이터
        auth_info: 인증 정보
        
    Returns:
        DeliveryRegisterResponse: 배송 등록 응답
        
    Raises:
        HTTPException: 배송 등록 실패 시
    """
    try:
        result = await mall_service.register_single_delivery(request, auth_info)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryRegisterResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Single delivery registration failed: {e}")
        raise HTTPException(status_code=500, detail="Single delivery registration failed")


@router.post("/deliveryListRegister", response_model=MultipleDeliveryRegisterResponse)
async def register_multiple_deliveries(
    request: MultipleDeliveryRegisterRequest,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> MultipleDeliveryRegisterResponse:
    """
    다중 배송을 등록합니다.
    
    Args:
        request: 다중 배송 등록 요청 데이터
        auth_info: 인증 정보
        
    Returns:
        MultipleDeliveryRegisterResponse: 다중 배송 등록 응답
        
    Raises:
        HTTPException: 다중 배송 등록 실패 시
    """
    try:
        result = await mall_service.register_multiple_deliveries(request, auth_info)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return MultipleDeliveryRegisterResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Multiple delivery registration failed: {e}")
        raise HTTPException(status_code=500, detail="Multiple delivery registration failed")


@router.get("/delivery/{invoice_number}", response_model=DeliveryTrackingResponse)
async def track_delivery(
    invoice_number: str,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryTrackingResponse:
    """
    배송을 추적합니다.
    
    Args:
        invoice_number: 송장번호
        auth_info: 인증 정보
        
    Returns:
        DeliveryTrackingResponse: 배송 추적 응답
        
    Raises:
        HTTPException: 배송 추적 실패 시
    """
    try:
        result = await mall_service.track_delivery_status(invoice_number, auth_info)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryTrackingResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery tracking failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery tracking failed")


@router.get("/possibleDelivery", response_model=DeliveryAvailabilityResponse)
async def check_delivery_availability(
    zipcode: str = Query(..., description="우편번호"),
    delivery_date: str = Query(..., alias="deliveryDate", description="배송 예정일 (YYYY-MM-DD)"),
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryAvailabilityResponse:
    """
    배송 가능 여부를 확인합니다.
    
    Args:
        zipcode: 우편번호
        delivery_date: 배송 예정일
        auth_info: 인증 정보
        
    Returns:
        DeliveryAvailabilityResponse: 배송 가능 여부 응답
        
    Raises:
        HTTPException: 배송 가능 여부 확인 실패 시
    """
    try:
        result = await mall_service.check_delivery_availability(
            zipcode=zipcode,
            delivery_date=delivery_date,
            auth_info=auth_info
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryAvailabilityResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery availability check failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery availability check failed")


@router.post("/delivery/{invoice_number}/cancel", response_model=DeliveryCancelResponse)
async def cancel_delivery(
    invoice_number: str,
    cancel_reason: str = Query(..., description="취소 사유"),
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryCancelResponse:
    """
    배송을 취소합니다.
    
    Args:
        invoice_number: 송장번호
        cancel_reason: 취소 사유
        auth_info: 인증 정보
        
    Returns:
        DeliveryCancelResponse: 배송 취소 응답
        
    Raises:
        HTTPException: 배송 취소 실패 시
    """
    try:
        result = await mall_service.cancel_delivery(
            invoice_number=invoice_number,
            cancel_reason=cancel_reason,
            auth_info=auth_info
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryCancelResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery cancellation failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery cancellation failed")


@router.post("/delivery/return", response_model=DeliveryReturnResponse)
async def request_return_delivery(
    request: DeliveryReturnRequest,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryReturnResponse:
    """
    반품 배송을 요청합니다.
    
    Args:
        request: 반품 배송 요청 데이터
        auth_info: 인증 정보
        
    Returns:
        DeliveryReturnResponse: 반품 배송 응답
        
    Raises:
        HTTPException: 반품 배송 요청 실패 시
    """
    try:
        result = await mall_service.request_return_delivery(request, auth_info)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryReturnResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Return delivery request failed: {e}")
        raise HTTPException(status_code=500, detail="Return delivery request failed")


@router.get("/delivery/{invoice_number}/history")
async def get_delivery_history(
    invoice_number: str,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> Dict[str, Any]:
    """
    배송 이력을 조회합니다.
    
    Args:
        invoice_number: 송장번호
        auth_info: 인증 정보
        
    Returns:
        Dict[str, Any]: 배송 이력 정보
        
    Raises:
        HTTPException: 배송 이력 조회 실패 시
    """
    try:
        # 배송 추적과 동일한 로직 사용 (이력 포함)
        result = await mall_service.track_delivery_status(invoice_number, auth_info)
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery history retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery history retrieval failed")


@router.put("/delivery/{invoice_number}/status")
async def update_delivery_status(
    invoice_number: str,
    status: str = Query(..., description="업데이트할 배송 상태"),
    auth_info: AuthInfo = Depends(get_auth_info)
) -> Dict[str, Any]:
    """
    배송 상태를 업데이트합니다.
    
    Args:
        invoice_number: 송장번호
        status: 업데이트할 상태
        auth_info: 인증 정보
        
    Returns:
        Dict[str, Any]: 상태 업데이트 결과
        
    Raises:
        HTTPException: 상태 업데이트 실패 시
    """
    try:
        # 이 기능은 mall_service에서 구현해야 할 추가 메서드
        # 현재는 기본 응답 반환
        result = {
            "success": True,
            "message": "Status update feature not implemented yet",
            "data": {
                "invoice_number": invoice_number,
                "new_status": status
            }
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Delivery status update failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery status update failed")