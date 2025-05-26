import pytest
from unittest.mock import AsyncMock, patch

from app.services.mall_service import MallService
from app.repositories.mall_repository import MallRepository # To mock its methods
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    MallApiDeliveryDTO,
    GoodsDTO,
    MallApiReturnDTO,
    GoodsNoDawnDTO, # Make sure this is imported
)
from typing import Optional # For possible_delivery

@pytest.fixture
def mock_mall_repository():
    mock_repo = AsyncMock(spec=MallRepository)
    # Configure default return values for pass-through methods
    mock_repo.cancel_delivery = AsyncMock(return_value="delivery_cancelled")
    mock_repo.find_by_invoice = AsyncMock(return_value="invoice_found")
    mock_repo.find_by_invoice_list = AsyncMock(return_value="invoice_list_found")
    mock_repo.delivery_list_register = AsyncMock(return_value="list_registered")
    mock_repo.delivery_register = AsyncMock(return_value="delivery_registered")
    mock_repo.possible_delivery = AsyncMock(return_value="delivery_possible_checked")
    mock_repo.return_delivery = AsyncMock(return_value="delivery_returned")
    mock_repo.return_list_register = AsyncMock(return_value="return_list_registered")
    mock_repo.return_register = AsyncMock(return_value="return_registered")
    mock_repo.close = AsyncMock()
    return mock_repo

@pytest.fixture
def mall_service(mock_mall_repository: AsyncMock):
    with patch('app.services.mall_service.MallRepository', return_value=mock_mall_repository) as patched_repo:
        service = MallService()
        service.repository = mock_mall_repository # Ensure mock is used
        return service

@pytest.mark.asyncio
async def test_cancel_delivery(mall_service: MallService, mock_mall_repository: AsyncMock):
    dto_arg = GoodsReturnRequestDTO(invoiceNumber="INV001")
    token_arg = "mall_token_cancel"
    
    expected_response = "cancel_op_done"
    mock_mall_repository.cancel_delivery.return_value = expected_response

    response = await mall_service.cancel_delivery(dto=dto_arg, token=token_arg)

    mock_mall_repository.cancel_delivery.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_find_by_invoice(mall_service: MallService, mock_mall_repository: AsyncMock):
    invoice_arg = "INV002"
    token_arg = "mall_token_find"

    expected_response = "invoice_data_found"
    mock_mall_repository.find_by_invoice.return_value = expected_response
    
    response = await mall_service.find_by_invoice(invoice_number=invoice_arg, token=token_arg)

    mock_mall_repository.find_by_invoice.assert_called_once_with(invoice_number=invoice_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_possible_delivery(mall_service: MallService, mock_mall_repository: AsyncMock):
    address_arg = "123 Test Address"
    token_arg = "mall_token_possible"
    postal_code_arg = "12345"
    dawn_delivery_arg = "Y"

    expected_response = "delivery_is_possible"
    mock_mall_repository.possible_delivery.return_value = expected_response

    response = await mall_service.possible_delivery(
        address=address_arg,
        token=token_arg,
        postal_code=postal_code_arg,
        dawn_delivery=dawn_delivery_arg
    )

    mock_mall_repository.possible_delivery.assert_called_once_with(
        address=address_arg,
        token=token_arg,
        postal_code=postal_code_arg,
        dawn_delivery=dawn_delivery_arg
    )
    assert response == expected_response
    
@pytest.mark.asyncio
async def test_possible_delivery_minimal_args(mall_service: MallService, mock_mall_repository: AsyncMock):
    address_arg = "456 Another Address"
    token_arg = "mall_token_possible_min"

    expected_response = "delivery_check_minimal"
    mock_mall_repository.possible_delivery.return_value = expected_response

    response = await mall_service.possible_delivery(address=address_arg, token=token_arg)

    mock_mall_repository.possible_delivery.assert_called_once_with(
        address=address_arg, token=token_arg, postal_code=None, dawn_delivery=None
    )
    assert response == expected_response


@pytest.mark.asyncio
async def test_close_repository(mall_service: MallService, mock_mall_repository: AsyncMock):
    await mall_service.close_repository()
    mock_mall_repository.close.assert_called_once()

# --- Completed tests for remaining methods ---

@pytest.mark.asyncio
async def test_find_by_invoice_list(mall_service: MallService, mock_mall_repository: AsyncMock):
    invoice_list_arg = "INV001,INV002"
    token_arg = "mall_token_find_list"
    
    expected_response = "invoice_list_data_here"
    mock_mall_repository.find_by_invoice_list.return_value = expected_response

    response = await mall_service.find_by_invoice_list(invoice_number_list=invoice_list_arg, token=token_arg)

    mock_mall_repository.find_by_invoice_list.assert_called_once_with(
        invoice_number_list=invoice_list_arg, token=token_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_delivery_list_register(mall_service: MallService, mock_mall_repository: AsyncMock):
    goods_item_data = {
        "deliveryAddress": "RegAddr", "deliveryName": "RegName",
        "deliveryPhone": "0987654321", "mallName": "RegMall"
    }
    dto_arg = MallApiDeliveryDTO(goodsList=[GoodsNoDawnDTO(**goods_item_data)]) 
    token_arg = "mall_token_dlr"

    expected_response = "delivery_list_registered_ok"
    mock_mall_repository.delivery_list_register.return_value = expected_response

    response = await mall_service.delivery_list_register(dto=dto_arg, token=token_arg)

    mock_mall_repository.delivery_list_register.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_delivery_register(mall_service: MallService, mock_mall_repository: AsyncMock):
    dto_arg = GoodsDTO(
        deliveryAddress="SingleRegAddr", deliveryName="SingleRegName",
        deliveryPhone="1122334455", mallName="SingleRegMall", dawnDelivery="N"
    )
    token_arg = "mall_token_dr"

    expected_response = "single_delivery_registered_ok"
    mock_mall_repository.delivery_register.return_value = expected_response

    response = await mall_service.delivery_register(dto=dto_arg, token=token_arg)

    mock_mall_repository.delivery_register.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_return_delivery(mall_service: MallService, mock_mall_repository: AsyncMock):
    dto_arg = GoodsReturnRequestDTO(invoiceNumber="INV_RETURN_002")
    token_arg = "mall_token_return_del"

    expected_response = "return_delivery_processed"
    mock_mall_repository.return_delivery.return_value = expected_response

    response = await mall_service.return_delivery(dto=dto_arg, token=token_arg)

    mock_mall_repository.return_delivery.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_return_list_register(mall_service: MallService, mock_mall_repository: AsyncMock):
    goods_item_data = {
        "deliveryAddress": "ReturnListAddr", "deliveryName": "ReturnListName",
        "deliveryPhone": "2233445566", "mallName": "ReturnListMall"
    }
    dto_arg = MallApiReturnDTO(goodsList=[GoodsNoDawnDTO(**goods_item_data)])
    token_arg = "mall_token_rlr"

    expected_response = "return_list_registered_ok"
    mock_mall_repository.return_list_register.return_value = expected_response

    response = await mall_service.return_list_register(dto=dto_arg, token=token_arg)

    mock_mall_repository.return_list_register.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_return_register(mall_service: MallService, mock_mall_repository: AsyncMock):
    dto_arg = GoodsNoDawnDTO(
        deliveryAddress="SingleReturnAddr", deliveryName="SingleReturnName",
        deliveryPhone="3344556677", mallName="SingleReturnMall"
    )
    token_arg = "mall_token_rr"

    expected_response = "single_return_registered_ok"
    mock_mall_repository.return_register.return_value = expected_response

    response = await mall_service.return_register(dto=dto_arg, token=token_arg)

    mock_mall_repository.return_register.assert_called_once_with(dto=dto_arg, token=token_arg)
    assert response == expected_response
