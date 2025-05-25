"""FastAPI router for Mall endpoints."""
from fastapi import APIRouter, Header, Depends, Query
from ..schemas import models
from ..services.mall_service import MallService
from ..repositories.remote_repository import TodayPickupRepository

router = APIRouter(prefix="/mall", tags=["mall"])

async def get_service() -> MallService:
    repo = TodayPickupRepository()
    return MallService(repo)

@router.post("/cancelDelivery")
async def cancel_delivery(data: models.GoodsReturnRequestDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.cancel_delivery(headers, data)

@router.get("/delivery/{invoice_number}")
async def get_delivery(invoice_number: str, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.get_delivery(headers, invoice_number)

@router.get("/deliveryList/{invoice_number_list}")
async def get_delivery_list(invoice_number_list: str, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.get_delivery_list(headers, invoice_number_list)

@router.post("/deliveryListRegister")
async def register_delivery_list(data: models.MallApiDeliveryDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.register_delivery_list(headers, data)

@router.post("/deliveryRegister")
async def register_delivery(data: models.GoodsDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.register_delivery(headers, data)

@router.get("/possibleDelivery")
async def possible_delivery(address: str = Query(...), postalCode: str = Query(None), dawnDelivery: str = Query(None), Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.possible_delivery(headers, address, postal_code=postalCode, dawn_delivery=dawnDelivery)

@router.post("/returnDelivery")
async def return_delivery(data: models.GoodsReturnRequestDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.return_delivery(headers, data)

@router.post("/returnListRegister")
async def register_return_list(data: models.MallApiReturnDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.register_return_list(headers, data)

@router.post("/returnRegister")
async def register_return(data: models.GoodsNoDawnDTO, Authorization: str = Header(...), service: MallService = Depends(get_service)):
    headers = {"Authorization": Authorization}
    return await service.register_return(headers, data)
