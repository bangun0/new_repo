"""
This module defines the repository class for interacting with the
MALL-specific endpoints of the Kakao T TodayPickup API.
It handles the construction and execution of HTTP requests to these endpoints.
"""
from typing import Optional, List 
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    MallApiDeliveryDTO,
    GoodsDTO,
    MallApiReturnDTO, 
    GoodsNoDawnDTO
)
from .base_repository import BaseRepository

class MallRepository(BaseRepository):
    """
    Repository for MALL Open API endpoints.

    This class extends `BaseRepository` and provides methods to interact
    with all mall-related API operations.
    """
    def __init__(self):
        """Initializes the MallRepository with the default base URL."""
        super().__init__()

    async def cancel_delivery(
        self, dto: GoodsReturnRequestDTO, token: str
    ) -> str:
        """
        Cancels a previously registered delivery. (배송취소)
        Calls POST /api/mall/cancelDelivery.
        OperationId: cancelDeliveryUsingPOST.

        Args:
            dto: DTO containing the invoice number of the delivery to cancel.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/cancelDelivery",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def find_by_invoice(self, invoice_number: str, token: str) -> str:
        """
        Retrieves delivery information for a single invoice number. (단건 배송조회)
        Calls GET /api/mall/delivery/{invoiceNumber}.
        OperationId: findByInvoiceUsingGET.

        Args:
            invoice_number: The invoice number to query.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API, typically containing delivery details.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "GET",
            f"/api/mall/delivery/{invoice_number}",
            headers=headers,
        )
        return response.text

    async def find_by_invoice_list(
        self, invoice_number_list: str, token: str
    ) -> str:
        """
        Retrieves delivery information for a list of invoice numbers. (다건 배송조회)
        Calls GET /api/mall/deliveryList/{invoiceNumberList}.
        OperationId: findByInvoiceListUsingGET.

        Args:
            invoice_number_list: Comma-separated string of invoice numbers (e.g., "01,02").
            token: The Authorization token for the mall.

        Returns:
            A string response from the API, typically containing delivery details for multiple invoices.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "GET",
            f"/api/mall/deliveryList/{invoice_number_list}",
            headers=headers,
        )
        return response.text

    async def delivery_list_register(
        self, dto: MallApiDeliveryDTO, token: str
    ) -> str:
        """
        Registers multiple deliveries in a single request. (다건 배송 등록)
        Calls POST /api/mall/deliveryListRegister.
        OperationId: deliveryListRegisterUsingPOST.

        Args:
            dto: DTO containing a list of goods for delivery and dawn delivery option.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/deliveryListRegister",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def delivery_register(self, dto: GoodsDTO, token: str) -> str:
        """
        Registers a single delivery. (단건 배송 등록)
        Calls POST /api/mall/deliveryRegister.
        OperationId: deliveryRegisterUsingPOST.

        Args:
            dto: DTO containing the details of the goods for delivery.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/deliveryRegister",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def possible_delivery(
        self,
        address: str,
        token: str,
        postal_code: Optional[str] = None,
        dawn_delivery: Optional[str] = None,
    ) -> str:
        """
        Checks if delivery is possible for a given address. (배송가능여부)
        Calls GET /api/mall/possibleDelivery.
        OperationId: possibleDeliveryUsingGET.

        Args:
            address: The address to check for delivery possibility.
            token: The Authorization token for the mall.
            postal_code: Optional postal code.
            dawn_delivery: Optional flag for dawn delivery (Y/N).

        Returns:
            A string response from the API, indicating delivery possibility.
        """
        headers = {"Authorization": token}
        params = {"address": address}
        if postal_code:
            params["postalCode"] = postal_code
        if dawn_delivery:
            params["dawnDelivery"] = dawn_delivery
        
        response = await self._request(
            "GET", "/api/mall/possibleDelivery", params=params, headers=headers
        )
        return response.text

    async def return_delivery(
        self, dto: GoodsReturnRequestDTO, token: str
    ) -> str:
        """
        Requests a return for a delivered item. (반품 요청)
        Calls POST /api/mall/returnDelivery.
        OperationId: returnDeliveryUsingPOST.

        Args:
            dto: DTO containing the invoice number of the item to be returned.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/returnDelivery",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def return_list_register(
        self, dto: MallApiReturnDTO, token: str
    ) -> str:
        """
        Registers multiple return/pickup requests in a single call. (다건 수거 등록)
        Calls POST /api/mall/returnListRegister.
        OperationId: returnListRegisterUsingPOST.

        Args:
            dto: DTO containing a list of goods to be returned/picked up.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/returnListRegister",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def return_register(self, dto: GoodsNoDawnDTO, token: str) -> str:
        """
        Registers a single return/pickup request. (단건 수거 등록)
        Calls POST /api/mall/returnRegister.
        OperationId: returnRegisterUsingPOST.

        Args:
            dto: DTO containing the details of the goods to be returned/picked up.
            token: The Authorization token for the mall.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token}
        response = await self._request(
            "POST",
            "/api/mall/returnRegister",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text
