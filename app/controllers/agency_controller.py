"""
대리점(Agency) Controller
대리점 관련 FastAPI 엔드포인트를 정의합니다.
"""
from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Header, Query, Depends
import logging

from app.services.agency_service import AgencyService
from app.models.base import AuthInfo
from app.schemas.agency import (
    TokenGenerationRequest,
    TokenGenerationResponse,
    TokenValidationRequest,
    TokenValidationResponse,
    DeliveryAssignmentRequest,
    DeliveryAssignmentResponse,
    DeliveryInfoRequest,
    DeliveryInfoResponse
)

logger = logging.getLogger(__name__)

# APIRouter 인스턴스 생성
router = APIRouter()

# AgencyService 인스턴스
agency_service = AgencyService()


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
    대리점 서비스 상태 확인
    
    Returns:
        Dict[str, Any]: 서비스 상태 정보
    """
    try:
        result = await agency_service.health_check()
        return result
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service health check failed")


@router.post("/auth/token", response_model=TokenGenerationResponse)
async def generate_token(request: TokenGenerationRequest) -> TokenGenerationResponse:
    """
    인증 토큰을 생성합니다.
    
    Args:
        request: 토큰 생성 요청 데이터
        
    Returns:
        TokenGenerationResponse: 토큰 생성 응답
        
    Raises:
        HTTPException: 토큰 생성 실패 시
    """
    try:
        result = await agency_service.generate_authentication_token(
            agency_id=request.agency_id,
            api_key=request.api_key
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return TokenGenerationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token generation failed: {e}")
        raise HTTPException(status_code=500, detail="Token generation failed")


@router.post("/auth", response_model=TokenValidationResponse)
async def validate_token(
    request: TokenValidationRequest,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> TokenValidationResponse:
    """
    토큰 유효성을 검증합니다.
    
    Args:
        request: 토큰 검증 요청 데이터
        auth_info: 인증 정보
        
    Returns:
        TokenValidationResponse: 토큰 검증 응답
        
    Raises:
        HTTPException: 토큰 검증 실패 시
    """
    try:
        result = await agency_service.validate_authentication_token(
            token=request.token,
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
        
        return TokenValidationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        raise HTTPException(status_code=500, detail="Token validation failed")


@router.put("/delivery", response_model=DeliveryAssignmentResponse)
async def assign_delivery(
    request: DeliveryAssignmentRequest,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> DeliveryAssignmentResponse:
    """
    배송을 기사에게 배정합니다.
    
    Args:
        request: 배송 배정 요청 데이터
        auth_info: 인증 정보
        
    Returns:
        DeliveryAssignmentResponse: 배송 배정 응답
        
    Raises:
        HTTPException: 배송 배정 실패 시
    """
    try:
        result = await agency_service.assign_delivery_to_driver(
            invoice_number=request.invoice_number,
            auth_info=auth_info,
            driver_id=request.driver_id,
            driver_name=request.driver_name,
            driver_phone=request.driver_phone,
            estimated_delivery_time=request.estimated_delivery_time
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryAssignmentResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery assignment failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery assignment failed")


@router.post("/delivery/list/{delivery_date}", response_model=DeliveryInfoResponse)
async def get_delivery_list(
    delivery_date: str,
    auth_info: AuthInfo = Depends(get_auth_info),
    status: Optional[str] = Query(None, description="배송 상태 필터"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(10, ge=1, le=100, description="페이지 크기")
) -> DeliveryInfoResponse:
    """
    배송 정보 목록을 조회합니다.
    
    Args:
        delivery_date: 배송일자 (YYYY-MM-DD)
        auth_info: 인증 정보
        status: 배송 상태 필터
        page: 페이지 번호
        size: 페이지 크기
        
    Returns:
        DeliveryInfoResponse: 배송 정보 목록 응답
        
    Raises:
        HTTPException: 배송 정보 조회 실패 시
    """
    try:
        result = await agency_service.get_delivery_information_list(
            delivery_date=delivery_date,
            auth_info=auth_info,
            status=status,
            page=page,
            size=size
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": result["message"],
                    "error_code": result["error_code"]
                }
            )
        
        return DeliveryInfoResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delivery list retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Delivery list retrieval failed")


@router.get("/postalcode/{zipcode}")
async def get_postal_code_info(
    zipcode: str,
    auth_info: AuthInfo = Depends(get_auth_info)
) -> Dict[str, Any]:
    """
    우편번호 정보를 조회합니다.
    
    Args:
        zipcode: 우편번호
        auth_info: 인증 정보
        
    Returns:
        Dict[str, Any]: 우편번호 정보
        
    Raises:
        HTTPException: 우편번호 정보 조회 실패 시
    """
    try:
        result = await agency_service.get_postal_code_information(
            zipcode=zipcode,
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
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Postal code info retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Postal code info retrieval failed")