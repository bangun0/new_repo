"""
This module provides the service layer for agency-related operations.
It encapsulates the business logic and interacts with the AgencyRepository
to perform data operations related to the AGENCY Open API.
"""
from app.repositories.agency_repository import AgencyRepository
from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeListDTO
)

class AgencyService:
    """
    Provides business logic for agency-related operations.

    This service interacts with the AgencyRepository to fetch and manipulate
    agency-related data from the external Kakao T TodayPickup API.
    It is responsible for handling any business rules or data transformations
    before passing data to or from the repository.
    """
    def __init__(self):
        """
        Initializes the AgencyService with an instance of AgencyRepository.
        The repository handles the direct communication with the external API.
        """
        # In a production application, the repository might be injected using
        # FastAPI's dependency injection system (e.g., via `Depends`) to improve
        # testability and decoupling. For this project, it's directly instantiated.
        self.repository = AgencyRepository()

    async def check_auth(self, token: str, agency_id: str) -> str:
        """
        Checks the authentication status for a given agency using their token.

        This method calls the corresponding method in the AgencyRepository.

        Args:
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository, typically indicating authentication success or failure.
        """
        # Currently, this is a direct pass-through to the repository.
        # Business logic (e.g., custom error handling, response parsing/transformation)
        # could be added here if needed.
        return await self.repository.check_auth(token=token, agency_id=agency_id)

    async def create_token(
        self,
        auth_dto: AuthAgencyDTO,
        authorization_header: str,
        agency_id: str
    ) -> str:
        """
        Requests the creation of a new authentication token for an agency.

        This method calls the corresponding method in the AgencyRepository.

        Args:
            auth_dto: Data Transfer Object containing credentials (accessKey, nonce, timestamp).
            authorization_header: The specific 'Authorization' header required by the token creation endpoint.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository, typically the newly generated token.
        """
        return await self.repository.create_token(
            auth_dto=auth_dto,
            authorization_header=authorization_header,
            agency_id=agency_id
        )

    async def update_delivery_ext_order_id(
        self,
        dto: DeliveryAgencyUpdateConsignDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Updates the external order ID or other details for a specific delivery. (배정완료)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            dto: DTO containing the delivery update information.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository.
        """
        return await self.repository.update_delivery_ext_order_id(
            dto=dto, token=token, agency_id=agency_id
        )

    async def return_delivery_flex(
        self,
        dto: DeliveryInvoiceNumberDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Transfers a delivery to the Flex system. (플렉스 이관)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            dto: DTO containing the invoice number of the delivery.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository.
        """
        return await self.repository.return_delivery_flex(
            dto=dto, token=token, agency_id=agency_id
        )

    async def return_delivery_list_flex(
        self,
        dto: DeliveryAgencyFlexListUpdateDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Transfers a list of deliveries to the Flex system. (플렉스 다건 이관)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            dto: DTO containing a list of invoice numbers.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository.
        """
        return await self.repository.return_delivery_list_flex(
            dto=dto, token=token, agency_id=agency_id
        )

    async def find_delivery_list(
        self,
        delivery_dt: str,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Finds and retrieves a list of deliveries for a specific date. (배송정보 조회)

        This method calls the corresponding method in the AgencyRepository.
        Any pre-processing of `delivery_dt` (e.g., date validation) could be added here.

        Args:
            delivery_dt: The delivery date in 'YYYY-MM-DD' format.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository, typically containing delivery information.
        """
        return await self.repository.find_delivery_list(
            delivery_dt=delivery_dt, token=token, agency_id=agency_id
        )

    async def update_delivery_state(
        self,
        dto: DeliveryAgencyStateUpdateDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Updates the status of a specific delivery. (배송상태 수정)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            dto: DTO containing the invoice number and new state information.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository.
        """
        return await self.repository.update_delivery_state(
            dto=dto, token=token, agency_id=agency_id
        )

    async def find_delivery_by_invoice_list(
        self,
        invoice_number_list: str,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Finds and retrieves delivery information for a list of invoice numbers. (운송장 배송조회)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            invoice_number_list: A comma-separated string of invoice numbers.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository, typically containing delivery information.
        """
        return await self.repository.find_delivery_by_invoice_list(
            invoice_number_list=invoice_number_list, token=token, agency_id=agency_id
        )

    async def save_postal_codes(
        self,
        dto: PostalCodeListDTO,
        token: str,
        agency_id: str,
    ) -> str:
        """
        Saves a list of postal codes and their delivery availability for an agency. (배송가능 구역 입력)

        This method calls the corresponding method in the AgencyRepository.

        Args:
            dto: DTO containing the list of postal codes and dawn delivery option.
            token: The agency's authorization token.
            agency_id: The agency's unique identifier.

        Returns:
            A string response from the repository.
        """
        return await self.repository.save_postal_codes(
            dto=dto, token=token, agency_id=agency_id
        )

    async def close_repository(self):
        """
        Closes the underlying HTTP client in the repository.
        This is important for releasing resources gracefully during application shutdown.
        """
        await self.repository.close()
