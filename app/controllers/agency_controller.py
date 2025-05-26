"""
This module defines the API endpoints for agency-related operations.
It uses FastAPI's APIRouter to group these endpoints and delegates the
business logic to the AgencyService.
"""
from fastapi import APIRouter, Depends, Header, Path, Body, Request 
from typing import Annotated 

from app.services.agency_service import AgencyService
from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeListDTO
)
# from fastapi.responses import PlainTextResponse # Example if plain text responses are needed

# Dependency function to get the AgencyService instance from the application state.
# This ensures that the same service instance (and thus repository and HTTP client)
# is used throughout the lifespan of the application, managed by `app/main.py`'s lifespan context.
def get_agency_service(request: Request) -> AgencyService:
    """
    Retrieves the shared AgencyService instance from the application state.
    This service instance is managed by the application's lifespan events.
    """
    return request.app.state.agency_service

# APIRouter for agency-specific endpoints.
# The prefix "/agency" will be added by the main app router, resulting in paths like /api/agency/...
router = APIRouter(
    prefix="/agency", # This prefix is applied in main.py when including the router.
    tags=["AGENCY Open Api"], # Tag for grouping in API documentation
)

@router.post("/auth")
async def check_auth_endpoint(
    authorization: Annotated[str, Header(description="Authorization token (Bearer token).")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Validates an agency's authentication token. (Token 유효성 검사)
    Corresponds to POST /api/agency/auth.

    The `Authorization` and `agencyId` headers are extracted and passed to the service.
    """
    # The service method is expected to return a string, which FastAPI will serialize as JSON.
    # If the external API strictly expects 'text/plain', a PlainTextResponse would be used.
    response_data = await service.check_auth(token=authorization, agency_id=agency_id)
    return response_data

@router.post("/auth/token")
async def create_token_endpoint(
    auth_dto: Annotated[AuthAgencyDTO, Body(description="Authentication credentials for token creation.")],
    authorization: Annotated[str, Header(description="Specific Authorization header required for token creation endpoint.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Generates a new authentication token for an agency. (토큰 생성)
    Corresponds to POST /api/agency/auth/token.

    Requires credentials in the request body and specific headers.
    """
    response_data = await service.create_token(
        auth_dto=auth_dto,
        authorization_header=authorization, # Note: This is a specific auth header for this endpoint
        agency_id=agency_id
    )
    return response_data

@router.put("/delivery")
async def update_delivery_ext_order_id_endpoint(
    dto: Annotated[DeliveryAgencyUpdateConsignDTO, Body(description="Delivery update information.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Updates delivery external order ID, consignee information, or status. (배정완료)
    Corresponds to PUT /api/agency/delivery.
    """
    response_data = await service.update_delivery_ext_order_id(
        dto=dto, token=authorization, agency_id=agency_id
    )
    return response_data

@router.put("/delivery/flex")
async def return_delivery_flex_endpoint(
    dto: Annotated[DeliveryInvoiceNumberDTO, Body(description="Invoice number for Flex transfer.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Transfers a delivery to the Flex system. (플렉스 이관)
    Corresponds to PUT /api/agency/delivery/flex.
    """
    response_data = await service.return_delivery_flex(
        dto=dto, token=authorization, agency_id=agency_id
    )
    return response_data

@router.put("/delivery/list/flex")
async def return_delivery_list_flex_endpoint(
    dto: Annotated[DeliveryAgencyFlexListUpdateDTO, Body(description="List of invoice numbers for Flex transfer.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Transfers multiple deliveries to the Flex system. (플렉스 다건 이관)
    Corresponds to PUT /api/agency/delivery/list/flex.
    """
    response_data = await service.return_delivery_list_flex(
        dto=dto, token=authorization, agency_id=agency_id
    )
    return response_data

@router.post("/delivery/list/{delivery_dt}") # Changed deliveryDt to delivery_dt
async def find_delivery_list_endpoint(
    delivery_dt: Annotated[str, Path(description="Delivery date in YYYY-MM-DD format.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Finds and retrieves a list of deliveries for a specific date. (배송정보 조회)
    Corresponds to POST /api/agency/delivery/list/{deliveryDt}.
    The delivery date is passed as a path parameter.
    """
    response_data = await service.find_delivery_list(
        delivery_dt=delivery_dt, token=authorization, agency_id=agency_id
    )
    return response_data

@router.put("/delivery/state")
async def update_delivery_state_endpoint(
    dto: Annotated[DeliveryAgencyStateUpdateDTO, Body(description="Delivery state update information.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Updates the status of a specific delivery. (배송상태 수정)
    Corresponds to PUT /api/agency/delivery/state.
    """
    response_data = await service.update_delivery_state(
        dto=dto, token=authorization, agency_id=agency_id
    )
    return response_data

@router.post("/delivery/{invoice_number_list}") # Changed invoiceNumberList to invoice_number_list
async def find_delivery_by_invoice_list_endpoint(
    invoice_number_list: Annotated[str, Path(description="Comma-separated list of invoice numbers.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Finds and retrieves delivery information for a list of invoice numbers. (운송장 배송조회)
    Corresponds to POST /api/agency/delivery/{invoiceNumberList}.
    Invoice numbers are passed as a comma-separated string in the path.
    """
    response_data = await service.find_delivery_by_invoice_list(
        invoice_number_list=invoice_number_list, token=authorization, agency_id=agency_id
    )
    return response_data

@router.post("/postal/save")
async def save_postal_codes_endpoint(
    dto: Annotated[PostalCodeListDTO, Body(description="List of postal codes and dawn delivery option.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    agency_id: Annotated[str, Header(description="Agency ID.", alias="agencyId")],
    service: AgencyService = Depends(get_agency_service)
):
    """
    Saves a list of postal codes and their delivery availability for an agency. (배송가능 구역 입력)
    Corresponds to POST /api/agency/postal/save.
    """
    response_data = await service.save_postal_codes(
        dto=dto, token=authorization, agency_id=agency_id
    )
    return response_data
