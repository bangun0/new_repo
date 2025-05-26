"""
배송 관련 모델 클래스
배송 정보를 나타내는 데이터 모델들을 정의합니다.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.models.base import BaseModel


class DeliveryStatus(Enum):
    """배송 상태 열거형"""
    PENDING = "pending"          # 배송 대기
    ASSIGNED = "assigned"        # 배송사 배정
    IN_TRANSIT = "in_transit"    # 배송 중
    DELIVERED = "delivered"      # 배송 완료
    CANCELLED = "cancelled"      # 배송 취소
    RETURNED = "returned"        # 반품


@dataclass
class DeliveryAddress:
    """
    배송 주소 정보 모델
    """
    zipcode: str                 # 우편번호
    address: str                 # 기본 주소
    address_detail: str          # 상세 주소
    receiver_name: str           # 수취인 이름
    receiver_phone: str          # 수취인 전화번호
    
    # 선택적 필드
    receiver_phone2: Optional[str] = None    # 수취인 추가 전화번호
    memo: Optional[str] = None               # 배송 메모


@dataclass
class DeliveryItem:
    """
    배송 상품 정보 모델
    """
    item_name: str               # 상품명
    quantity: int                # 수량
    price: int                   # 가격
    
    # 선택적 필드
    item_code: Optional[str] = None          # 상품 코드
    option: Optional[str] = None             # 상품 옵션


@dataclass
class Delivery(BaseModel):
    """
    배송 정보 모델
    """
    invoice_number: str          # 송장번호
    delivery_dt: str             # 배송일자 (YYYY-MM-DD)
    status: DeliveryStatus       # 배송 상태
    address: DeliveryAddress     # 배송 주소
    items: List[DeliveryItem]    # 배송 상품 목록
    
    # 선택적 필드
    mall_order_number: Optional[str] = None  # 쇼핑몰 주문번호
    delivery_fee: Optional[int] = None       # 배송비
    cod_amount: Optional[int] = None         # 착불 금액
    estimated_delivery_time: Optional[str] = None  # 예상 배송 시간
    actual_delivery_time: Optional[datetime] = None  # 실제 배송 시간
    agency_id: Optional[str] = None          # 배송사 ID
    driver_name: Optional[str] = None        # 기사 이름
    driver_phone: Optional[str] = None       # 기사 전화번호


@dataclass
class DeliveryTracking:
    """
    배송 추적 정보 모델
    """
    invoice_number: str          # 송장번호
    current_status: DeliveryStatus  # 현재 상태
    tracking_history: List[dict]    # 배송 추적 이력
    last_updated: datetime          # 마지막 업데이트 시간
    
    # 선택적 필드
    estimated_delivery: Optional[datetime] = None  # 예상 배송 완료 시간


@dataclass
class PostalCode:
    """
    우편번호 정보 모델
    """
    zipcode: str                 # 우편번호
    sido: str                    # 시도
    sigungu: str                 # 시군구
    dong: str                    # 동
    is_deliverable: bool         # 배송 가능 여부
    delivery_fee: Optional[int] = None  # 배송비