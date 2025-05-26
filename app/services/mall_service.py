"""
This module provides the service layer for mall-related operations.
It encapsulates the business logic and interacts with the MallRepository
to perform data operations related to the MALL Open API.
"""
from app.repositories.mall_repository import MallRepository
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    MallApiDeliveryDTO,
    GoodsDTO,
    MallApiReturnDTO,
    GoodsNoDawnDTO
)
from typing import Optional # For possible_delivery method

class MallService:
    """
    Provides business logic for mall-related operations.

    This service interacts with the MallRepository to fetch and manipulate
    mall-related data from the external Kakao T TodayPickup API.
    It is responsible for handling any business rules or data transformations
    before passing data to or from the repository.
    """
    def __init__(self):
        """
        Initializes the MallService with an instance of MallRepository.
        The repository handles the direct communication with the external API.
        """
        # In a production application, the repository might be injected using
        # FastAPI's dependency injection system (e.g., via `Depends`) to improve
        # testability and decoupling. For this project, it's directly instantiated.
        self.repository = MallRepository()

    async def cancel_delivery(self, dto: GoodsReturnRequestDTO, token: str) -> str:
        """
        Cancels a previously registered delivery for a mall. (배송취소)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing the invoice number of the delivery to cancel.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.cancel_delivery(dto=dto, token=token)

    async def find_by_invoice(self, invoice_number: str, token: str) -> str:
        """
        Finds and retrieves delivery information by a single invoice number for a mall. (단건 배송조회)

        This method calls the corresponding method in the MallRepository.

        Args:
            invoice_number: The invoice number to search for.
            token: The mall's authorization token.

        Returns:
            A string response from the repository, typically containing delivery details.
        """
        return await self.repository.find_by_invoice(
            invoice_number=invoice_number, token=token
        )

    async def find_by_invoice_list(
        self, invoice_number_list: str, token: str
    ) -> str:
        """
        Finds and retrieves delivery information for a list of invoice numbers for a mall. (다건 배송조회)

        This method calls the corresponding method in the MallRepository.

        Args:
            invoice_number_list: A comma-separated string of invoice numbers.
            token: The mall's authorization token.

        Returns:
            A string response from the repository, typically containing delivery details.
        """
        return await self.repository.find_by_invoice_list(
            invoice_number_list=invoice_number_list, token=token
        )

    async def delivery_list_register(
        self, dto: MallApiDeliveryDTO, token: str
    ) -> str:
        """
        Registers multiple deliveries in a single request for a mall. (다건 배송 등록)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing a list of goods for delivery and dawn delivery option.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.delivery_list_register(dto=dto, token=token)

    async def delivery_register(self, dto: GoodsDTO, token: str) -> str:
        """
        Registers a single delivery for a mall. (단건 배송 등록)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing the details of the goods for delivery.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.delivery_register(dto=dto, token=token)

    async def possible_delivery(
        self,
        address: str,
        token: str,
        postal_code: Optional[str] = None,
        dawn_delivery: Optional[str] = None,
    ) -> str:
        """
        Checks if delivery is possible for a given address for a mall. (배송가능여부)

        This method calls the corresponding method in the MallRepository.

        Args:
            address: The address to check.
            token: The mall's authorization token.
            postal_code: Optional postal code for more specific checking.
            dawn_delivery: Optional flag ('Y'/'N') to check for dawn delivery capability.

        Returns:
            A string response from the repository, indicating delivery possibility.
        """
        return await self.repository.possible_delivery(
            address=address,
            token=token,
            postal_code=postal_code,
            dawn_delivery=dawn_delivery,
        )

    async def return_delivery(self, dto: GoodsReturnRequestDTO, token: str) -> str:
        """
        Requests a return for a previously delivered item for a mall. (반품 요청)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing the invoice number of the item to be returned.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.return_delivery(dto=dto, token=token)

    async def return_list_register(
        self, dto: MallApiReturnDTO, token: str
    ) -> str:
        """
        Registers multiple return/pickup requests in a single call for a mall. (다건 수거 등록)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing a list of goods to be returned/picked up.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.return_list_register(dto=dto, token=token)

    async def return_register(self, dto: GoodsNoDawnDTO, token: str) -> str:
        """
        Registers a single return/pickup request for a mall. (단건 수거 등록)

        This method calls the corresponding method in the MallRepository.

        Args:
            dto: DTO containing the details of the goods to be returned/picked up.
            token: The mall's authorization token.

        Returns:
            A string response from the repository.
        """
        return await self.repository.return_register(dto=dto, token=token)

    async def close_repository(self):
        """
        Closes the underlying HTTP client in the repository.
        This is important for releasing resources gracefully during application shutdown.
        """
        await self.repository.close()
