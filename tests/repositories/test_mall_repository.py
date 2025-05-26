import pytest
import pytest_asyncio # Import the asyncio fixture decorator
from unittest.mock import AsyncMock, patch

from httpx import Response, HTTPStatusError, RequestError

from app.repositories.mall_repository import MallRepository
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO,
    MallApiDeliveryDTO,
    GoodsDTO,
    MallApiReturnDTO,
    GoodsNoDawnDTO # Ensure this is imported for return_register
)

BASE_URL = "https://admin.todaypickup.com" # Should match BaseRepository's default

@pytest_asyncio.fixture # Use the correct decorator
async def mall_repository():
    repo = MallRepository()
    repo.client = AsyncMock(spec=repo.client)
    # repo.base_url = BASE_URL # Not needed if BaseRepository handles it.
    yield repo
    await repo.close()

@pytest.mark.asyncio
async def test_cancel_delivery_success(mall_repository: MallRepository):
    mock_response_text = "cancel_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None
    
    dto = GoodsReturnRequestDTO(invoiceNumber="INV123")
    token_param = "bearer_mall_token"

    result = await mall_repository.cancel_delivery(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/cancelDelivery", 
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_find_by_invoice_success(mall_repository: MallRepository):
    mock_response_text = "invoice_data"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    invoice_number_param = "INV789"
    token_param = "bearer_mall_token_find"

    result = await mall_repository.find_by_invoice(invoice_number=invoice_number_param, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "GET",
        f"/api/mall/delivery/{invoice_number_param}", 
        json=None,
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_possible_delivery_success(mall_repository: MallRepository):
    mock_response_text = "possible_true"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    token_param = "bearer_mall_token_possible"
    address_param = "123 Test St"
    postal_code_param = "12345"
    dawn_delivery_param = "Y"

    result = await mall_repository.possible_delivery(
        address=address_param,
        token=token_param,
        postal_code=postal_code_param,
        dawn_delivery=dawn_delivery_param
    )

    expected_params = {
        "address": address_param,
        "postalCode": postal_code_param,
        "dawnDelivery": dawn_delivery_param,
    }
    mall_repository.client.request.assert_called_once_with(
        "GET",
        "/api/mall/possibleDelivery", 
        json=None,
        params=expected_params,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_possible_delivery_only_address(mall_repository: MallRepository):
    mock_response_text = "possible_false"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    token_param = "bearer_mall_token_possible_min"
    address_param = "456 Other Ave"

    result = await mall_repository.possible_delivery(address=address_param, token=token_param)

    expected_params = {"address": address_param}
    mall_repository.client.request.assert_called_once_with(
        "GET",
        "/api/mall/possibleDelivery", 
        json=None,
        params=expected_params,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text
    
@pytest.mark.asyncio
async def test_mall_repository_http_status_error(mall_repository: MallRepository):
    mock_request_for_error = AsyncMock() 
    mock_request_for_error.url = "/api/mall/delivery/any_invoice"

    mall_repository.client.request.side_effect = HTTPStatusError(
        message="Mall API Client Error", request=mock_request_for_error, response=AsyncMock(status_code=403)
    )
    with pytest.raises(HTTPStatusError):
        await mall_repository.find_by_invoice(invoice_number="any_invoice", token="any_token")

@pytest.mark.asyncio
async def test_mall_repository_request_error(mall_repository: MallRepository):
    mock_request_for_error = AsyncMock()
    mock_request_for_error.url = "/api/mall/delivery/any_invoice"

    mall_repository.client.request.side_effect = RequestError(
        message="Mall API Network Error", request=mock_request_for_error
    )
    with pytest.raises(RequestError):
        await mall_repository.find_by_invoice(invoice_number="any_invoice", token="any_token")

# --- Added tests for remaining methods ---

@pytest.mark.asyncio
async def test_find_by_invoice_list_success(mall_repository: MallRepository):
    mock_response_text = "invoice_list_data"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    invoice_list_param = "INV001,INV002,INV003"
    token_param = "bearer_mall_token_find_list"

    result = await mall_repository.find_by_invoice_list(invoice_number_list=invoice_list_param, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "GET",
        f"/api/mall/deliveryList/{invoice_list_param}", # Relative path
        json=None,
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_delivery_list_register_success(mall_repository: MallRepository):
    mock_response_text = "delivery_list_register_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    goods_item_data = {
        "deliveryAddress": "Test Addr", "deliveryName": "Test Name",
        "deliveryPhone": "1234567890", "mallName": "Test Mall"
    }
    # MallApiDeliveryDTO uses GoodsNoDawnDTO for its goodsList
    dto = MallApiDeliveryDTO(
        goodsList=[GoodsNoDawnDTO(**goods_item_data)], # Corrected to GoodsNoDawnDTO
        dawnDelivery="N"
    )
    token_param = "bearer_mall_token_dlr"

    result = await mall_repository.delivery_list_register(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/deliveryListRegister", # Relative path
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_delivery_register_success(mall_repository: MallRepository):
    mock_response_text = "delivery_register_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None
    
    dto = GoodsDTO(
        deliveryAddress="12 Main St", deliveryName="Register Test",
        deliveryPhone="0987654321", mallName="RegMall", dawnDelivery="Y"
    )
    token_param = "bearer_mall_token_dr"

    result = await mall_repository.delivery_register(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/deliveryRegister", # Relative path
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_return_delivery_success(mall_repository: MallRepository):
    mock_response_text = "return_delivery_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    dto = GoodsReturnRequestDTO(invoiceNumber="INV_RETURN_001")
    token_param = "bearer_mall_token_return"

    result = await mall_repository.return_delivery(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/returnDelivery", # Relative path
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_return_list_register_success(mall_repository: MallRepository):
    mock_response_text = "return_list_register_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    goods_item_data = {
        "deliveryAddress": "Return Addr List", "deliveryName": "Return Name List",
        "deliveryPhone": "1122334455", "mallName": "Return Mall List"
    }
    # MallApiReturnDTO uses GoodsNoDawnDTO for its goodsList
    dto = MallApiReturnDTO(goodsList=[GoodsNoDawnDTO(**goods_item_data)])
    token_param = "bearer_mall_token_rlr"

    result = await mall_repository.return_list_register(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/returnListRegister", # Relative path
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_return_register_success(mall_repository: MallRepository):
    mock_response_text = "return_register_success"
    mall_repository.client.request.return_value = AsyncMock(spec=Response, text=mock_response_text, status_code=200)
    mall_repository.client.request.return_value.raise_for_status = lambda: None

    dto = GoodsNoDawnDTO(
        deliveryAddress="Single Return Addr", deliveryName="Single Return Name",
        deliveryPhone="5566778899", mallName="Single Return Mall"
    )
    token_param = "bearer_mall_token_rr"

    result = await mall_repository.return_register(dto=dto, token=token_param)

    mall_repository.client.request.assert_called_once_with(
        "POST",
        "/api/mall/returnRegister", # Relative path
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param},
    )
    assert result == mock_response_text
