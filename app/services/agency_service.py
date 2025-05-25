"""Service layer for AGENCY APIs."""
from typing import Dict, Any
from ..repositories.remote_repository import TodayPickupRepository
from ..schemas import models

class AgencyService:
    """Business logic for agency related operations."""

    def __init__(self, repository: TodayPickupRepository):
        self.repo = repository

    async def auth(self, headers: Dict[str, str]) -> Any:
        resp = await self.repo.request("POST", "/api/agency/auth", headers)
        return resp.json()

    async def auth_token(self, headers: Dict[str, str], data: models.AuthAgencyDTO) -> Any:
        resp = await self.repo.request("POST", "/api/agency/auth/token", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def update_delivery(self, headers: Dict[str, str], data: models.DeliveryAgencyUpdateConsignDTO) -> Any:
        resp = await self.repo.request("PUT", "/api/agency/delivery", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def return_flex(self, headers: Dict[str, str], data: models.DeliveryInvoiceNumberDTO) -> Any:
        resp = await self.repo.request("PUT", "/api/agency/delivery/flex", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def return_flex_list(self, headers: Dict[str, str], data: models.DeliveryAgencyFlexListUpdateDTO) -> Any:
        resp = await self.repo.request("PUT", "/api/agency/delivery/list/flex", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def find_delivery_list(self, headers: Dict[str, str], delivery_dt: str) -> Any:
        path = f"/api/agency/delivery/list/{delivery_dt}"
        resp = await self.repo.request("POST", path, headers)
        return resp.json()

    async def update_delivery_state(self, headers: Dict[str, str], data: models.DeliveryAgencyStateUpdateDTO) -> Any:
        resp = await self.repo.request("PUT", "/api/agency/delivery/state", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def find_delivery(self, headers: Dict[str, str], invoice_list: str) -> Any:
        path = f"/api/agency/delivery/{invoice_list}"
        resp = await self.repo.request("POST", path, headers)
        return resp.json()

    async def save_postal(self, headers: Dict[str, str], data: models.PostalCodeListDTO) -> Any:
        resp = await self.repo.request("POST", "/api/agency/postal/save", headers, json=data.dict(by_alias=True))
        return resp.json()
