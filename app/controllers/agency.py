"""FastAPI router for Agency endpoints."""
from fastapi import APIRouter, Header, Depends
from ..schemas import models
from ..services.agency_service import AgencyService
from ..repositories.remote_repository import TodayPickupRepository

router = APIRouter(prefix="/agency", tags=["agency"])

# Dependency for service
async def get_service() -> AgencyService:
    repo = TodayPickupRepository()
    return AgencyService(repo)

@router.post("/auth")
async def check_auth(Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.auth(headers)

@router.post("/auth/token")
async def create_token(data: models.AuthAgencyDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.auth_token(headers, data)

@router.put("/delivery")
async def update_delivery(data: models.DeliveryAgencyUpdateConsignDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.update_delivery(headers, data)

@router.put("/delivery/flex")
async def return_delivery_flex(data: models.DeliveryInvoiceNumberDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.return_flex(headers, data)

@router.put("/delivery/list/flex")
async def return_delivery_list_flex(data: models.DeliveryAgencyFlexListUpdateDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.return_flex_list(headers, data)

@router.post("/delivery/list/{delivery_dt}")
async def find_delivery_list(delivery_dt: str, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.find_delivery_list(headers, delivery_dt)

@router.put("/delivery/state")
async def update_delivery_state(data: models.DeliveryAgencyStateUpdateDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.update_delivery_state(headers, data)

@router.post("/delivery/{invoice_number_list}")
async def find_delivery(invoice_number_list: str, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.find_delivery(headers, invoice_number_list)

@router.post("/postal/save")
async def postal_save(data: models.PostalCodeListDTO, Authorization: str = Header(...), agencyId: str = Header(...), service: AgencyService = Depends(get_service)):
    headers = {"Authorization": Authorization, "agencyId": agencyId}
    return await service.save_postal(headers, data)
