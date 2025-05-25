"""Service layer for MALL APIs."""
from typing import Dict, Any
from ..repositories.remote_repository import TodayPickupRepository
from ..schemas import models

class MallService:
    """Business logic for mall related operations."""

    def __init__(self, repository: TodayPickupRepository):
        self.repo = repository

    async def cancel_delivery(self, headers: Dict[str, str], data: models.GoodsReturnRequestDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/cancelDelivery", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def get_delivery(self, headers: Dict[str, str], invoice_number: str) -> Any:
        path = f"/api/mall/delivery/{invoice_number}"
        resp = await self.repo.request("GET", path, headers)
        return resp.json()

    async def get_delivery_list(self, headers: Dict[str, str], invoice_list: str) -> Any:
        path = f"/api/mall/deliveryList/{invoice_list}"
        resp = await self.repo.request("GET", path, headers)
        return resp.json()

    async def register_delivery_list(self, headers: Dict[str, str], data: models.MallApiDeliveryDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/deliveryListRegister", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def register_delivery(self, headers: Dict[str, str], data: models.GoodsDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/deliveryRegister", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def possible_delivery(self, headers: Dict[str, str], address: str, postal_code: str = None, dawn_delivery: str = None) -> Any:
        params = {"address": address}
        if postal_code:
            params["postalCode"] = postal_code
        if dawn_delivery:
            params["dawnDelivery"] = dawn_delivery
        resp = await self.repo.client.get("/api/mall/possibleDelivery", headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def return_delivery(self, headers: Dict[str, str], data: models.GoodsReturnRequestDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/returnDelivery", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def register_return_list(self, headers: Dict[str, str], data: models.MallApiReturnDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/returnListRegister", headers, json=data.dict(by_alias=True))
        return resp.json()

    async def register_return(self, headers: Dict[str, str], data: models.GoodsNoDawnDTO) -> Any:
        resp = await self.repo.request("POST", "/api/mall/returnRegister", headers, json=data.dict(by_alias=True))
        return resp.json()
