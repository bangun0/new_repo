"""
대리점(Agency) API 관련 스키마
대리점 API 요청/응답을 위한 Pydantic 모델들을 정의합니다.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseRequest, BaseResponse


class TokenGenerationRequest(BaseRequest):
    """
    토큰 생성 요청 스키마
    """
    agency_id: str = Field(..., description="대리점 ID")
    api_key: str = Field(..., description="API 키")


class TokenGenerationResponse(BaseResponse):
    """
    토큰 생성 응답 스키마
    """
    access_token: Optional[str] = Field(None, description="액세스 토큰")
    token_type: Optional[str] = Field(None, description="토큰 타입")
    expires_in: Optional[int] = Field(None, description="토큰 만료 시간(초)")


class TokenValidationRequest(BaseRequest):
    """
    토큰 검증 요청 스키마
    """
    token: str = Field(..., description="검증할 토큰")


class TokenValidationResponse(BaseResponse):
    """
    토큰 검증 응답 스키마
    """
    is_valid: Optional[bool] = Field(None, description="토큰 유효 여부")
    expires_at: Optional[datetime] = Field(None, description="토큰 만료 시간")
    agency_id: Optional[str] = Field(None, description="대리점 ID")


class DeliveryAssignmentRequest(BaseRequest):
    """
    배송 배정 요청 스키마
    """
    invoice_number: str = Field(..., description="송장번호")
    driver_id: Optional[str] = Field(None, description="기사 ID")
    driver_name: Optional[str] = Field(None, description="기사 이름")
    driver_phone: Optional[str] = Field(None, description="기사 전화번호")
    estimated_delivery_time: Optional[str] = Field(None, description="예상 배송 시간")


class DeliveryAssignmentResponse(BaseResponse):
    """
    배송 배정 응답 스키마
    """
    invoice_number: Optional[str] = Field(None, description="송장번호")
    assigned_at: Optional[datetime] = Field(None, description="배정 시간")


class DeliveryInfoRequest(BaseRequest):
    """
    배송 정보 조회 요청 스키마
    """
    delivery_date: str = Field(..., description="배송일자 (YYYY-MM-DD)")
    status: Optional[str] = Field(None, description="배송 상태")
    page: Optional[int] = Field(1, description="페이지 번호")
    size: Optional[int] = Field(10, description="페이지 크기")


class DeliveryInfo(BaseModel):
    """
    배송 정보 스키마
    """
    invoice_number: str = Field(..., description="송장번호")
    mall_order_number: Optional[str] = Field(None, description="쇼핑몰 주문번호")
    delivery_date: str = Field(..., description="배송일자")
    status: str = Field(..., description="배송 상태")
    receiver_name: str = Field(..., description="수취인 이름")
    receiver_phone: str = Field(..., description="수취인 전화번호")
    address: str = Field(..., description="배송 주소")
    zipcode: str = Field(..., description="우편번호")
    item_name: str = Field(..., description="상품명")
    quantity: int = Field(..., description="수량")
    delivery_fee: Optional[int] = Field(None, description="배송비")
    cod_amount: Optional[int] = Field(None, description="착불 금액")
    memo: Optional[str] = Field(None, description="배송 메모")


class DeliveryInfoResponse(BaseResponse):
    """
    배송 정보 조회 응답 스키마
    """
    deliveries: Optional[List[DeliveryInfo]] = Field(None, description="배송 정보 목록")
    total_count: Optional[int] = Field(None, description="전체 건수")
    page: Optional[int] = Field(None, description="현재 페이지")
    total_pages: Optional[int] = Field(None, description="전체 페이지 수")