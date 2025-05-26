import pytest
import pytest_asyncio # Import the asyncio fixture decorator
from unittest.mock import AsyncMock, patch

from httpx import Response, HTTPStatusError, RequestError

from app.repositories.agency_repository import AgencyRepository
from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeListDTO,
    PostalCodeSaveDTO
)

BASE_URL = "https://admin.todaypickup.com" # This is the default in BaseRepository

@pytest_asyncio.fixture # Use the correct decorator
async def agency_repository():
    repo = AgencyRepository()
    # Replace the client with a mock for testing repository logic without real HTTP calls
    # We also mock the base_url to ensure our test calls match the expected URLs
    repo.client = AsyncMock(spec=repo.client) 
    repo.base_url = BASE_URL # Ensure the fixture uses the same BASE_URL for assertions
    yield repo
    await repo.close() # Ensure client.aclose is called if it were real

@pytest.mark.asyncio
async def test_check_auth_success(agency_repository: AgencyRepository):
    mock_response_text = "auth_success_token"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    # Mock raise_for_status to do nothing for successful calls
    agency_repository.client.request.return_value.raise_for_status = lambda: None


    token_param = "bearer_token_123"
    agency_id_param = "agency_abc"
    
    result = await agency_repository.check_auth(token=token_param, agency_id=agency_id_param)

    agency_repository.client.request.assert_called_once_with(
        "POST",
        "/api/agency/auth", # Endpoint is relative to base_url in _request method
        json=None, # No body for this request
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_create_token_success(agency_repository: AgencyRepository):
    mock_response_text = "new_generated_token"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    auth_dto = AuthAgencyDTO(accessKey="key", nonce="nonce", timestamp="ts")
    auth_header = "auth_header_val"
    agency_id_param = "agency_xyz"

    result = await agency_repository.create_token(
        auth_dto=auth_dto,
        authorization_header=auth_header,
        agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "POST",
        "/api/agency/auth/token", # Endpoint is relative to base_url
        json=auth_dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": auth_header, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_repository_http_status_error(agency_repository: AgencyRepository):
    # Mock the request to raise an HTTPStatusError
    # The actual request object might be needed by httpx.HTTPStatusError
    mock_request_for_error = AsyncMock() 
    mock_request_for_error.url = "/api/agency/auth" # Example URL

    agency_repository.client.request.side_effect = HTTPStatusError(
        message="Client Error", request=mock_request_for_error, response=AsyncMock(status_code=400)
    )
    
    with pytest.raises(HTTPStatusError):
        await agency_repository.check_auth(token="any_token", agency_id="any_agency_id")

@pytest.mark.asyncio
async def test_repository_request_error(agency_repository: AgencyRepository):
    # Mock the request to raise a RequestError (e.g., network issue)
    mock_request_for_error = AsyncMock()
    mock_request_for_error.url = "/api/agency/auth" # Example URL

    agency_repository.client.request.side_effect = RequestError(
        message="Network Error", request=mock_request_for_error
    )
    
    with pytest.raises(RequestError):
        await agency_repository.check_auth(token="any_token", agency_id="any_agency_id")

@pytest.mark.asyncio
async def test_update_delivery_ext_order_id_success(agency_repository: AgencyRepository):
    mock_response_text = "update_success"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    dto = DeliveryAgencyUpdateConsignDTO(extOrderId="ext123", invoiceNumber="inv789", status="done")
    token_param = "token_for_put"
    agency_id_param = "agency_for_put"

    result = await agency_repository.update_delivery_ext_order_id(
        dto=dto, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "PUT",
        "/api/agency/delivery", # Endpoint is relative to base_url
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text
        
@pytest.mark.asyncio
async def test_find_delivery_list_success(agency_repository: AgencyRepository):
    mock_response_text = "delivery_list_data"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    delivery_dt_param = "2023-10-26"
    token_param = "token_for_find"
    agency_id_param = "agency_for_find"

    result = await agency_repository.find_delivery_list(
        delivery_dt=delivery_dt_param, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "POST",
        f"/api/agency/delivery/list/{delivery_dt_param}", # Endpoint is relative to base_url
        json=None, # No body for this POST as per API docs
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_return_delivery_flex_success(agency_repository: AgencyRepository):
    mock_response_text = "flex_return_success"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    dto = DeliveryInvoiceNumberDTO(invoiceNumber="invflex123")
    token_param = "token_flex"
    agency_id_param = "agency_flex"

    result = await agency_repository.return_delivery_flex(
        dto=dto, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "PUT",
        "/api/agency/delivery/flex",
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_return_delivery_list_flex_success(agency_repository: AgencyRepository):
    mock_response_text = "flex_list_return_success"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    dto = DeliveryAgencyFlexListUpdateDTO(invoiceNumberList=["invflex1", "invflex2"])
    token_param = "token_flex_list"
    agency_id_param = "agency_flex_list"

    result = await agency_repository.return_delivery_list_flex(
        dto=dto, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "PUT",
        "/api/agency/delivery/list/flex",
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_update_delivery_state_success(agency_repository: AgencyRepository):
    mock_response_text = "state_update_success"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    dto = DeliveryAgencyStateUpdateDTO(invoiceNumber="invstate1", status="DELIVERED", holdCode="H00")
    token_param = "token_state"
    agency_id_param = "agency_state"

    result = await agency_repository.update_delivery_state(
        dto=dto, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "PUT",
        "/api/agency/delivery/state",
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_find_delivery_by_invoice_list_success(agency_repository: AgencyRepository):
    mock_response_text = "invoice_list_data"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    invoice_list_param = "inv1,inv2,inv3"
    token_param = "token_invoice_find"
    agency_id_param = "agency_invoice_find"

    result = await agency_repository.find_delivery_by_invoice_list(
        invoice_number_list=invoice_list_param, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "POST",
        f"/api/agency/delivery/{invoice_list_param}",
        json=None,
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text

@pytest.mark.asyncio
async def test_save_postal_codes_success(agency_repository: AgencyRepository):
    mock_response_text = "postal_save_success"
    agency_repository.client.request.return_value = AsyncMock(spec=Response)
    agency_repository.client.request.return_value.text = mock_response_text
    agency_repository.client.request.return_value.status_code = 200
    agency_repository.client.request.return_value.raise_for_status = lambda: None

    postal_save_dto = PostalCodeSaveDTO(postNumber="12345", sido="서울", gugun="강남구", possibleArea="Y")
    dto = PostalCodeListDTO(postNumberSaveList=[postal_save_dto])
    token_param = "token_postal"
    agency_id_param = "agency_postal"

    result = await agency_repository.save_postal_codes(
        dto=dto, token=token_param, agency_id=agency_id_param
    )

    agency_repository.client.request.assert_called_once_with(
        "POST",
        "/api/agency/postal/save",
        json=dto.model_dump(exclude_none=True),
        params=None,
        headers={"Authorization": token_param, "agencyId": agency_id_param},
    )
    assert result == mock_response_text
