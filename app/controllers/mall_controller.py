"""
This module defines the API endpoints for mall-related operations.
It uses FastAPI's APIRouter to group these endpoints and delegates the
business logic to the MallService.
"""
from fastapi import APIRouter, Depends, Header, Path, Query, Body, Request
from typing import Annotated, Optional

from app.services.mall_service import MallService
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    MallApiDeliveryDTO,
    GoodsDTO,
    MallApiReturnDTO,
    GoodsNoDawnDTO
)

# Dependency function to get the MallService instance from the application state.
# This ensures that the same service instance (and thus repository and HTTP client)
# is used throughout the lifespan of the application, managed by `app/main.py`'s lifespan context.
def get_mall_service(request: Request) -> MallService:
    """
    Retrieves the shared MallService instance from the application state.
    This service instance is managed by the application's lifespan events.
    """
    return request.app.state.mall_service

# APIRouter for mall-specific endpoints.
# The prefix "/mall" will be added by the main app router, resulting in paths like /api/mall/...
router = APIRouter(
    prefix="/mall", # This prefix is applied in main.py when including the router.
    tags=["MALL Open Api"], # Tag for grouping in API documentation
)

@router.post("/cancelDelivery")
async def cancel_delivery_endpoint(
    dto: Annotated[GoodsReturnRequestDTO, Body(description="Invoice number of the delivery to cancel.")],
    authorization: Annotated[str, Header(description="Authorization token (Bearer token).")],
    service: MallService = Depends(get_mall_service)
):
    """
    Cancels a previously registered delivery. (배송취소)
    Corresponds to POST /api/mall/cancelDelivery.
    """
    response_data = await service.cancel_delivery(dto=dto, token=authorization)
    return response_data

@router.get("/delivery/{invoice_number}") # Changed invoiceNumber to invoice_number
async def find_by_invoice_endpoint(
    invoice_number: Annotated[str, Path(description="송장번호 - Invoice number to query.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Retrieves delivery information for a single invoice number. (단건 배송조회)
    Corresponds to GET /api/mall/delivery/{invoiceNumber}.
    """
    response_data = await service.find_by_invoice(
        invoice_number=invoice_number, token=authorization
    )
    return response_data

@router.get("/deliveryList/{invoice_number_list}") # Changed invoiceNumberList to invoice_number_list
async def find_by_invoice_list_endpoint(
    invoice_number_list: Annotated[str, Path(description="송장번호 리스트(ex 01,02) - Comma-separated list of invoice numbers.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Retrieves delivery information for a list of invoice numbers. (다건 배송조회)
    Corresponds to GET /api/mall/deliveryList/{invoiceNumberList}.
    """
    response_data = await service.find_by_invoice_list(
        invoice_number_list=invoice_number_list, token=authorization
    )
    return response_data

@router.post("/deliveryListRegister")
async def delivery_list_register_endpoint(
    dto: Annotated[MallApiDeliveryDTO, Body(description="List of goods for delivery and dawn delivery option.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Registers multiple deliveries in a single request. (다건 배송 등록)
    Corresponds to POST /api/mall/deliveryListRegister.
    """
    response_data = await service.delivery_list_register(dto=dto, token=authorization)
    return response_data

@router.post("/deliveryRegister")
async def delivery_register_endpoint(
    dto: Annotated[GoodsDTO, Body(description="Details of the goods for a single delivery.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Registers a single delivery. (단건 배송 등록)
    Corresponds to POST /api/mall/deliveryRegister.
    """
    response_data = await service.delivery_register(dto=dto, token=authorization)
    return response_data

@router.get("/possibleDelivery")
async def possible_delivery_endpoint(
    address: Annotated[str, Query(description="주소 - Address to check for delivery possibility.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    postal_code: Annotated[Optional[str], Query(description="우편번호 - Optional postal code.", alias="postalCode")] = None,
    dawn_delivery: Annotated[Optional[str], Query(description="새벽배송여부 - Optional Y/N flag for dawn delivery.", alias="dawnDelivery")] = None,
    service: MallService = Depends(get_mall_service)
):
    """
    Checks if delivery is possible for a given address. (배송가능여부)
    Corresponds to GET /api/mall/possibleDelivery.
    """
    response_data = await service.possible_delivery(
        address=address,
        token=authorization,
        postal_code=postal_code,
        dawn_delivery=dawn_delivery
    )
    return response_data

@router.post("/returnDelivery")
async def return_delivery_endpoint(
    dto: Annotated[GoodsReturnRequestDTO, Body(description="Invoice number of the item to be returned.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Requests a return for a delivered item. (반품 요청)
    Corresponds to POST /api/mall/returnDelivery.
    """
    response_data = await service.return_delivery(dto=dto, token=authorization)
    return response_data

@router.post("/returnListRegister")
async def return_list_register_endpoint(
    dto: Annotated[MallApiReturnDTO, Body(description="List of goods to be returned/picked up.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Registers multiple return/pickup requests in a single call. (다건 수거 등록)
    Corresponds to POST /api/mall/returnListRegister.
    """
    response_data = await service.return_list_register(dto=dto, token=authorization)
    return response_data

@router.post("/returnRegister")
async def return_register_endpoint(
    dto: Annotated[GoodsNoDawnDTO, Body(description="Details of the goods for a single return/pickup.")],
    authorization: Annotated[str, Header(description="Authorization token.")],
    service: MallService = Depends(get_mall_service)
):
    """
    Registers a single return/pickup request. (단건 수거 등록)
    Corresponds to POST /api/mall/returnRegister.
    """
    response_data = await service.return_register(dto=dto, token=authorization)
    return response_data
