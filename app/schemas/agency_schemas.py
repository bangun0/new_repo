"""
This module defines the Pydantic models used for data validation and serialization
for the AGENCY Open API endpoints. These models represent the expected request
and response structures for interactions with the agency-related parts of the
Kakao T TodayPickup API.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class AuthAgencyDTO(BaseModel):
    """
    Authentication details for agency.
    Used for operations like generating an authentication token.
    Corresponds to the request body for POST /api/agency/auth/token.
    """
    accessKey: Optional[str] = Field(None, description="API access key.")
    nonce: Optional[str] = Field(None, description="A unique number or string generated for each request.")
    timestamp: Optional[str] = Field(None, description="Request timestamp.")

class DeliveryAgencyUpdateConsignDTO(BaseModel):
    """
    DTO for updating consignee information or delivery status for a delivery by agency.
    Corresponds to the request body for PUT /api/agency/delivery.
    """
    extOrderId: Optional[str] = Field(None, description="External order ID.")
    invoiceNumber: Optional[str] = Field(None, description="Invoice number of the delivery.")
    status: Optional[str] = Field(None, description="Status of the delivery.")

class DeliveryInvoiceNumberDTO(BaseModel):
    """
    DTO containing a single invoice number.
    Used for operations like PUT /api/agency/delivery/flex.
    """
    invoiceNumber: Optional[str] = Field(None, description="Invoice number of the delivery.")

class DeliveryAgencyFlexListUpdateDTO(BaseModel):
    """
    DTO for updating a list of flexible delivery invoices by agency.
    Corresponds to the request body for PUT /api/agency/delivery/list/flex.
    """
    invoiceNumberList: Optional[List[str]] = Field(None, description="List of invoice numbers for flexible delivery update.")

class DeliveryAgencyStateUpdateDTO(BaseModel):
    """
    DTO for updating the state of a delivery by agency.
    Corresponds to the request body for PUT /api/agency/delivery/state.
    """
    holdCode: Optional[str] = Field(None, description="Hold code for the delivery.")
    imgUrl: Optional[str] = Field(None, description="Image URL related to the delivery state.")
    invoiceNumber: Optional[str] = Field(None, description="Invoice number of the delivery.")
    status: Optional[str] = Field(None, description="Status of the delivery.")

class PostalCodeSaveDTO(BaseModel):
    """
    DTO for individual postal code information to be saved by an agency.
    Used as an item in the list for POST /api/agency/postal/save.
    """
    buildingCode: Optional[str] = Field(None, description="Building identification code.")
    buildingName: Optional[str] = Field(None, description="Name of the building.")
    legalDongCode: Optional[str] = Field(None, description="Administrative district code (legal dong).")
    roadCode: Optional[str] = Field(None, description="Road name code.")
    roadName: Optional[str] = Field(None, description="Name of the road.")
    postNumber: str = Field(..., description="Postal code.")
    sido: str = Field(..., description="Province or metropolitan city name.", example="서울")
    gugun: str = Field(..., description="District name.", example="종로구")
    possibleArea: str = Field(..., description="Delivery availability (Y for available, N for unavailable).", example="Y")
    deliveryGroup: Optional[str] = Field(None, description="Delivery group code used by the company (for invoice printing).")
    adminDong: Optional[str] = Field(None, description="Administrative district name (admin dong).")
    legalDong: Optional[str] = Field(None, description="Legal district name (legal dong).")

class PostalCodeListDTO(BaseModel):
    """
    DTO for submitting a list of postal codes to be saved by an agency,
    including an option for dawn delivery.
    Corresponds to the request body for POST /api/agency/postal/save.
    """
    dawnDelivery: Optional[str] = Field("N", description="Dawn delivery availability (Y for yes, N for no, default N).", example="N")
    postNumberSaveList: List[PostalCodeSaveDTO] = Field(..., description="List of postal code information to save.")
