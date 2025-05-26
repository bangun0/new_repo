"""
쇼핑몰(Mall) API 관련 스키마
쇼핑몰 API 요청/응답을 위한 Pydantic 모델들을 정의합니다.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.schemas.base import BaseRequest, BaseResponse


class DeliveryItemSchema(BaseModel):
    """
    배송 상품 스키마
    """
    item_name: str = Field(..., description="상품명")
    quantity: int = Field(..., ge=1, description="수량")
    price: int = Field(..., ge=0, description="가격")
    item_code: Optional[str] = Field(None, description="상품 코드")
    option: Optional[str] = Field(None, description="상품 옵션")


class DeliveryAddressSchema(BaseModel):
    """
    배송 주소 스키마
    """
    zipcode: str = Field(..., description="우편번호")
    address: str = Field(..., description="기본 주소")
    address_detail: str = Field(..., description="상세 주소")
    receiver_name: str = Field(..., description="수취인 이름")
    receiver_phone: str = Field(..., description="수취인 전화번호")
    receiver_phone2: Optional[str] = Field(None, description="수취인 추가 전화번호")
    memo: Optional[str] = Field(None, description="배송 메모")


class SingleDeliveryRegisterRequest(BaseRequest):
    """
    단일 배송 등록 요청 스키마
    """
    mall_order_number: str = Field(..., description="쇼핑몰 주문번호")
    delivery_date: str = Field(..., description="배송 예정일 (YYYY-MM-DD)")
    address: DeliveryAddressSchema = Field(..., description="배송 주소")
    items: List[DeliveryItemSchema] = Field(..., description="배송 상품 목록")
    delivery_fee: Optional[int] = Field(0, ge=0, description="배송비")
    cod_amount: Optional[int] = Field(0, ge=0, description="착불 금액")
    
    @field_validator('delivery_date')
    @classmethod
    def validate_delivery_date(cls, v):
        """배송일자 형식 검증"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('배송일자는 YYYY-MM-DD 형식이어야 합니다')
        return v


class MultipleDeliveryRegisterRequest(BaseRequest):
    """
    다중 배송 등록 요청 스키마
    """
    deliveries: List[SingleDeliveryRegisterRequest] = Field(
        ..., 
        description="배송 목록",
        max_length=100
    )


class DeliveryRegisterResponse(BaseResponse):
    """
    배송 등록 응답 스키마
    """
    invoice_number: Optional[str] = Field(None, description="생성된 송장번호")
    mall_order_number: Optional[str] = Field(None, description="쇼핑몰 주문번호")
    registered_at: Optional[datetime] = Field(None, description="등록 시간")


class MultipleDeliveryRegisterResponse(BaseResponse):
    """
    다중 배송 등록 응답 스키마
    """
    registered_deliveries: Optional[List[DeliveryRegisterResponse]] = Field(
        None, 
        description="등록된 배송 목록"
    )
    failed_deliveries: Optional[List[dict]] = Field(
        None, 
        description="등록 실패한 배송 목록"
    )
    total_requested: Optional[int] = Field(None, description="요청된 총 건수")
    total_success: Optional[int] = Field(None, description="성공한 건수")
    total_failed: Optional[int] = Field(None, description="실패한 건수")


class DeliveryTrackingResponse(BaseResponse):
    """
    배송 추적 응답 스키마
    """
    invoice_number: Optional[str] = Field(None, description="송장번호")
    mall_order_number: Optional[str] = Field(None, description="쇼핑몰 주문번호")
    current_status: Optional[str] = Field(None, description="현재 배송 상태")
    delivery_date: Optional[str] = Field(None, description="배송일자")
    receiver_name: Optional[str] = Field(None, description="수취인 이름")
    receiver_phone: Optional[str] = Field(None, description="수취인 전화번호")
    address: Optional[str] = Field(None, description="배송 주소")
    driver_name: Optional[str] = Field(None, description="기사 이름")
    driver_phone: Optional[str] = Field(None, description="기사 전화번호")
    estimated_delivery_time: Optional[str] = Field(None, description="예상 배송 시간")
    actual_delivery_time: Optional[datetime] = Field(None, description="실제 배송 시간")
    tracking_history: Optional[List[dict]] = Field(None, description="배송 추적 이력")


class DeliveryAvailabilityRequest(BaseRequest):
    """
    배송 가능 여부 확인 요청 스키마
    """
    zipcode: str = Field(..., description="우편번호")
    delivery_date: str = Field(..., description="배송 예정일 (YYYY-MM-DD)")
    
    @field_validator('delivery_date')
    @classmethod
    def validate_delivery_date(cls, v):
        """배송일자 형식 검증"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('배송일자는 YYYY-MM-DD 형식이어야 합니다')
        return v


class DeliveryAvailabilityResponse(BaseResponse):
    """
    배송 가능 여부 확인 응답 스키마
    """
    zipcode: Optional[str] = Field(None, description="우편번호")
    is_deliverable: Optional[bool] = Field(None, description="배송 가능 여부")
    delivery_fee: Optional[int] = Field(None, description="배송비")
    estimated_delivery_days: Optional[int] = Field(None, description="예상 배송 소요일")
    area_name: Optional[str] = Field(None, description="배송 지역명")


class DeliveryCancelRequest(BaseRequest):
    """
    배송 취소 요청 스키마
    """
    invoice_number: str = Field(..., description="송장번호")
    cancel_reason: str = Field(..., description="취소 사유")


class DeliveryCancelResponse(BaseResponse):
    """
    배송 취소 응답 스키마
    """
    invoice_number: Optional[str] = Field(None, description="송장번호")
    cancelled_at: Optional[datetime] = Field(None, description="취소 시간")
    cancel_reason: Optional[str] = Field(None, description="취소 사유")


class DeliveryReturnRequest(BaseRequest):
    """
    반품 배송 요청 스키마
    """
    original_invoice_number: str = Field(..., description="원본 송장번호")
    return_address: DeliveryAddressSchema = Field(..., description="반품 주소")
    return_reason: str = Field(..., description="반품 사유")
    return_items: List[DeliveryItemSchema] = Field(..., description="반품 상품 목록")


class DeliveryReturnResponse(BaseResponse):
    """
    반품 배송 응답 스키마
    """
    return_invoice_number: Optional[str] = Field(None, description="반품 송장번호")
    original_invoice_number: Optional[str] = Field(None, description="원본 송장번호")
    return_registered_at: Optional[datetime] = Field(None, description="반품 등록 시간")