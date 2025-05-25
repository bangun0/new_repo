from pydantic import BaseModel, Field
from typing import List, Optional

class AuthAgencyDTO(BaseModel):
    access_key: Optional[str] = Field(None, alias="accessKey")
    nonce: Optional[str]
    timestamp: Optional[str]

class DeliveryAgencyUpdateConsignDTO(BaseModel):
    ext_order_id: Optional[str] = Field(None, alias="extOrderId")
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")
    status: Optional[str]

class DeliveryInvoiceNumberDTO(BaseModel):
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")

class DeliveryAgencyStateUpdateDTO(BaseModel):
    hold_code: Optional[str] = Field(None, alias="holdCode")
    img_url: Optional[str] = Field(None, alias="imgUrl")
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")
    status: Optional[str]

class DeliveryAgencyFlexListUpdateDTO(BaseModel):
    invoice_number_list: Optional[List[str]] = Field(None, alias="invoiceNumberList")

class PostalCodeSaveDTO(BaseModel):
    building_code: Optional[str] = Field(None, alias="buildingCode")
    building_name: Optional[str] = Field(None, alias="buildingName")
    legal_dong_code: Optional[str] = Field(None, alias="legalDongCode")
    road_code: Optional[str] = Field(None, alias="roadCode")
    road_name: Optional[str] = Field(None, alias="roadName")
    post_number: str = Field(..., alias="postNumber")
    sido: str
    gugun: str
    possible_area: str = Field(..., alias="possibleArea")
    delivery_group: Optional[str] = Field(None, alias="deliveryGroup")
    admin_dong: Optional[str] = Field(None, alias="adminDong")
    legal_dong: Optional[str] = Field(None, alias="legalDong")

class PostalCodeListDTO(BaseModel):
    dawn_delivery: Optional[str] = Field("N", alias="dawnDelivery")
    post_number_save_list: List[PostalCodeSaveDTO] = Field(..., alias="postNumberSaveList")

class GoodsReturnRequestDTO(BaseModel):
    invoice_number: str = Field(..., alias="invoiceNumber")

class GoodsNoDawnDTO(BaseModel):
    children_mall_id: Optional[str] = Field(None, alias="childrenMallId")
    delivery_address: str = Field(..., alias="deliveryAddress")
    delivery_address_eng: Optional[str] = Field(None, alias="deliveryAddressEng")
    delivery_message: Optional[str] = Field(None, alias="deliveryMessage")
    delivery_name: str = Field(..., alias="deliveryName")
    delivery_phone: str = Field(..., alias="deliveryPhone")
    delivery_postal: Optional[str] = Field(None, alias="deliveryPostal")
    delivery_tel: Optional[str] = Field(None, alias="deliveryTel")
    goods_name: Optional[str] = Field(None, alias="goodsName")
    invoice_number: Optional[str] = Field(None, alias="invoiceNumber")
    invoice_print_yn: Optional[str] = Field("N", alias="invoicePrintYn")
    mall_name: str = Field(..., alias="mallName")
    option_name: Optional[str] = Field(None, alias="optionName")
    order_number: Optional[str] = Field(None, alias="orderNumber")
    quantity: Optional[int]
    reserve_dt: Optional[str] = Field(None, alias="reserveDt")

class MallApiDeliveryDTO(BaseModel):
    dawn_delivery: Optional[str] = Field(None, alias="dawnDelivery")
    goods_list: List[GoodsNoDawnDTO] = Field(..., alias="goodsList")

class MallApiReturnDTO(BaseModel):
    goods_list: List[GoodsNoDawnDTO] = Field(..., alias="goodsList")

class GoodsDTO(GoodsNoDawnDTO):
    dawn_delivery: Optional[str] = Field(None, alias="dawnDelivery")
