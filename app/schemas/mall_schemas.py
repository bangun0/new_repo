"""
This module defines the Pydantic models used for data validation and serialization
for the MALL Open API endpoints. These models represent the expected request
and response structures for interactions with the mall-related parts of the
Kakao T TodayPickup API.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class GoodsReturnRequestDTO(BaseModel):
    """
    DTO for requesting goods return or canceling a delivery.
    Used as the request body for POST /api/mall/cancelDelivery and POST /api/mall/returnDelivery.
    """
    invoiceNumber: str = Field(..., description="Invoice number for the goods to be returned or canceled.")

class GoodsNoDawnDTO(BaseModel):
    """
    DTO for goods information, excluding the 'dawnDelivery' option.
    This model is a common structure used as items in lists within other DTOs like
    `MallApiReturnDTO` (for returnListRegister) and `MallApiDeliveryDTO` (for deliveryListRegister),
    and also for the request body of POST /api/mall/returnRegister.
    """
    childrenMallId: Optional[str] = Field(None, description="상점 아이디(관리 하는 상점 아이디) - Child mall ID, if applicable.")
    deliveryAddress: str = Field(..., description="수취인주소 - Recipient's address.")
    deliveryAddressEng: Optional[str] = Field(None, description="수취인주소영문 - Recipient's address in English.")
    deliveryMessage: Optional[str] = Field(None, description="배송 메시지 - Delivery message.")
    deliveryName: str = Field(..., description="수취인명 - Recipient's name.")
    deliveryPhone: str = Field(..., description="수취인 휴대폰 - Recipient's mobile phone number.")
    deliveryPostal: Optional[str] = Field(None, description="수취인 우편번호 - Recipient's postal code.")
    deliveryTel: Optional[str] = Field(None, description="수취인 전화번호 - Recipient's telephone number.")
    goodsName: Optional[str] = Field(None, description="상품명 - Product name.")
    invoiceNumber: Optional[str] = Field(None, description="송장 번호 (송장번호 개별 생성시 입력필요, 12자리여야 합니다) - Invoice number (required for individual invoice creation, must be 12 digits).")
    invoicePrintYn: Optional[str] = Field("N", description="송장 출력 여부 (Y,N(기본값)) - Invoice print status (Y/N, default is N).", example="N")
    mallName: str = Field(..., description="쇼핑몰_명 - Mall name.")
    optionName: Optional[str] = Field(None, description="옵션_명 - Product option name.")
    orderNumber: Optional[str] = Field(None, description="주문번호 - Order number.")
    quantity: Optional[int] = Field(None, description="수량 - Quantity.") # format: int32
    reserveDt: Optional[str] = Field(None, description="예약날짜 [YYYY-MM-DD] - Reservation date [YYYY-MM-DD].")

class MallApiReturnDTO(BaseModel):
    """
    DTO for mall API bulk return registration requests.
    Corresponds to the request body for POST /api/mall/returnListRegister.
    """
    goodsList: List[GoodsNoDawnDTO] = Field(..., description="상품_리스트 - List of goods to be returned.")

class MallApiDeliveryDTO(BaseModel):
    """
    DTO for mall API bulk delivery registration requests.
    Corresponds to the request body for POST /api/mall/deliveryListRegister.
    """
    dawnDelivery: Optional[str] = Field(None, description="새벽배송여부 - Dawn delivery option (Y/N).")
    goodsList: List[GoodsNoDawnDTO] = Field(..., description="상품_리스트 - List of goods for delivery.")

class GoodsDTO(BaseModel):
    """
    DTO for goods information, including the 'dawnDelivery' option.
    Used as the request body for single delivery registration (POST /api/mall/deliveryRegister).
    """
    childrenMallId: Optional[str] = Field(None, description="상점 아이디(관리 하는 상점 아이디) - Child mall ID, if applicable.")
    dawnDelivery: Optional[str] = Field(None, description="새벽배송여부 - Dawn delivery option (Y/N).")
    deliveryAddress: str = Field(..., description="수취인주소 - Recipient's address.")
    deliveryAddressEng: Optional[str] = Field(None, description="수취인주소영문 - Recipient's address in English.")
    deliveryMessage: Optional[str] = Field(None, description="배송 메시지 - Delivery message.")
    deliveryName: str = Field(..., description="수취인명 - Recipient's name.")
    deliveryPhone: str = Field(..., description="수취인 휴대폰 - Recipient's mobile phone number.")
    deliveryPostal: Optional[str] = Field(None, description="수취인 우편번호 - Recipient's postal code.")
    deliveryTel: Optional[str] = Field(None, description="수취인 전화번호 - Recipient's telephone number.")
    goodsName: Optional[str] = Field(None, description="상품명 - Product name.")
    invoiceNumber: Optional[str] = Field(None, description="송장 번호 (송장번호 개별 생성시 입력필요, 12자리여야 합니다) - Invoice number (required for individual invoice creation, must be 12 digits).")
    invoicePrintYn: Optional[str] = Field("N", description="송장 출력 여부 (Y,N(기본값)) - Invoice print status (Y/N, default is N).", example="N")
    mallName: str = Field(..., description="쇼핑몰_명 - Mall name.")
    optionName: Optional[str] = Field(None, description="옵션_명 - Product option name.")
    orderNumber: Optional[str] = Field(None, description="주문번호 - Order number.")
    quantity: Optional[int] = Field(None, description="수량 - Quantity.") # format: int32
    reserveDt: Optional[str] = Field(None, description="예약날짜 [YYYY-MM-DD] - Reservation date [YYYY-MM-DD].")
