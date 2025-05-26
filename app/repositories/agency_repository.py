"""
This module defines the repository class for interacting with the
AGENCY-specific endpoints of the Kakao T TodayPickup API.
It handles the construction and execution of HTTP requests to these endpoints.
"""
from typing import Optional
from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeListDTO
)
from .base_repository import BaseRepository

class AgencyRepository(BaseRepository):
    """
    Repository for AGENCY Open API endpoints.

    This class extends `BaseRepository` and provides methods to interact
    with all agency-related API operations.
    """
    def __init__(self):
        """Initializes the AgencyRepository with the default base URL."""
        super().__init__()

    async def check_auth(self, token: str, agency_id: str) -> str:
        """
        Validates an agency's authentication token.
        Calls POST /api/agency/auth.
        Corresponds to operationId: checkAuthUsingPOST.

        Args:
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API, typically indicating auth status.
        """
        headers = {
            "Authorization": token,
            "agencyId": agency_id,
        }
        response = await self._request("POST", "/api/agency/auth", headers=headers)
        return response.text 

    async def create_token(
        self, 
        auth_dto: AuthAgencyDTO, 
        authorization_header: str, # This is specifically the 'Authorization' for this endpoint itself
        agency_id: str
    ) -> str:
        """
        Generates a new authentication token for an agency.
        Calls POST /api/agency/auth/token.
        Corresponds to operationId: authTokenUsingPOST.

        Args:
            auth_dto: DTO containing accessKey, nonce, and timestamp.
            authorization_header: The specific Authorization header required for this token creation endpoint.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API, typically the new token.
        """
        headers = {
            "Authorization": authorization_header, 
            "agencyId": agency_id,
        }
        response = await self._request(
            "POST", 
            "/api/agency/auth/token", 
            data=auth_dto.model_dump(exclude_none=True), 
            headers=headers
        )
        return response.text

    async def update_delivery_ext_order_id(
        self,
        dto: DeliveryAgencyUpdateConsignDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Updates delivery external order ID, consignee info, or status. (배정완료)
        Calls PUT /api/agency/delivery.
        Corresponds to operationId: updateDeliveryExtOrderIdUsingPUT.

        Args:
            dto: DTO containing delivery update information.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "PUT",
            "/api/agency/delivery",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def return_delivery_flex(
        self,
        dto: DeliveryInvoiceNumberDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Transfers a delivery to Flex. (플렉스 이관)
        Calls PUT /api/agency/delivery/flex.
        Corresponds to operationId: returnDeliveryFlexUsingPUT.

        Args:
            dto: DTO containing the invoice number.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "PUT",
            "/api/agency/delivery/flex",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def return_delivery_list_flex(
        self,
        dto: DeliveryAgencyFlexListUpdateDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Transfers multiple deliveries to Flex. (플렉스 다건 이관)
        Calls PUT /api/agency/delivery/list/flex.
        Corresponds to operationId: returnDeliveryListFlexUsingPUT.

        Args:
            dto: DTO containing a list of invoice numbers.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "PUT",
            "/api/agency/delivery/list/flex",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def find_delivery_list(
        self,
        delivery_dt: str,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Finds a list of deliveries by date. (배송정보 조회)
        Calls POST /api/agency/delivery/list/{deliveryDt}.
        Corresponds to operationId: findDeliveryListUsingPOST.

        Args:
            delivery_dt: Delivery date in YYYY-MM-DD format.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API, typically containing delivery information.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "POST",
            f"/api/agency/delivery/list/{delivery_dt}",
            headers=headers,
        )
        return response.text

    async def update_delivery_state(
        self,
        dto: DeliveryAgencyStateUpdateDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Updates the state of a delivery. (배송상태 수정)
        Calls PUT /api/agency/delivery/state.
        Corresponds to operationId: updateDeliveryStateUsingPUT.

        Args:
            dto: DTO containing delivery state update information.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "PUT",
            "/api/agency/delivery/state",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text

    async def find_delivery_by_invoice_list(
        self,
        invoice_number_list: str, 
        token: str,
        agency_id: str,
    ) -> str:
        """
        Finds deliveries by a comma-separated list of invoice numbers. (운송장 배송조회)
        Calls POST /api/agency/delivery/{invoiceNumberList}.
        Corresponds to operationId: findDeliveryUsingPOST.

        Args:
            invoice_number_list: Comma-separated string of invoice numbers.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API, typically containing delivery information.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "POST",
            f"/api/agency/delivery/{invoice_number_list}",
            headers=headers,
        )
        return response.text

    async def save_postal_codes(
        self,
        dto: PostalCodeListDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Saves postal code information for an agency. (배송가능 구역 입력)
        Calls POST /api/agency/postal/save.
        Corresponds to operationId: postNumberSaveUsingPOST.

        Args:
            dto: DTO containing a list of postal codes and dawn delivery option.
            token: The Authorization token for the agency.
            agency_id: The ID of the agency.

        Returns:
            A string response from the API.
        """
        headers = {"Authorization": token, "agencyId": agency_id}
        response = await self._request(
            "POST",
            "/api/agency/postal/save",
            data=dto.model_dump(exclude_none=True),
            headers=headers,
        )
        return response.text
