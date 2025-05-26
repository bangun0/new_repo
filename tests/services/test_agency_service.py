import pytest
from unittest.mock import AsyncMock, patch

from app.services.agency_service import AgencyService
from app.repositories.agency_repository import AgencyRepository # To mock its methods
from app.schemas.agency_schemas import (
    AuthAgencyDTO,
    DeliveryAgencyUpdateConsignDTO,
    DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO,
    DeliveryAgencyStateUpdateDTO,
    PostalCodeListDTO,
    PostalCodeSaveDTO # Ensure this is imported for save_postal_codes test
)

@pytest.fixture
def mock_agency_repository():
    mock_repo = AsyncMock(spec=AgencyRepository)
    mock_repo.check_auth = AsyncMock(return_value="auth_checked")
    mock_repo.create_token = AsyncMock(return_value="token_created")
    mock_repo.update_delivery_ext_order_id = AsyncMock(return_value="delivery_updated")
    mock_repo.return_delivery_flex = AsyncMock(return_value="delivery_flexed")
    mock_repo.return_delivery_list_flex = AsyncMock(return_value="delivery_list_flexed")
    mock_repo.find_delivery_list = AsyncMock(return_value="delivery_list_found")
    mock_repo.update_delivery_state = AsyncMock(return_value="state_updated")
    mock_repo.find_delivery_by_invoice_list = AsyncMock(return_value="invoices_found")
    mock_repo.save_postal_codes = AsyncMock(return_value="postal_saved")
    mock_repo.close = AsyncMock()
    return mock_repo

@pytest.fixture
def agency_service(mock_agency_repository: AsyncMock):
    with patch('app.services.agency_service.AgencyRepository', return_value=mock_agency_repository) as patched_repo:
        service = AgencyService()
        service.repository = mock_agency_repository 
        return service

@pytest.mark.asyncio
async def test_check_auth(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    token_arg = "test_token"
    agency_id_arg = "test_agency_id"
    expected_response = "auth_checked_specific"
    mock_agency_repository.check_auth.return_value = expected_response
    response = await agency_service.check_auth(token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.check_auth.assert_called_once_with(token=token_arg, agency_id=agency_id_arg)
    assert response == expected_response

@pytest.mark.asyncio
async def test_create_token(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    auth_dto_arg = AuthAgencyDTO(accessKey="k", nonce="n", timestamp="t")
    auth_header_arg = "auth_header"
    agency_id_arg = "test_agency_id_token"
    expected_response = "token_created_specific"
    mock_agency_repository.create_token.return_value = expected_response
    response = await agency_service.create_token(
        auth_dto=auth_dto_arg,
        authorization_header=auth_header_arg,
        agency_id=agency_id_arg
    )
    mock_agency_repository.create_token.assert_called_once_with(
        auth_dto=auth_dto_arg,
        authorization_header=auth_header_arg,
        agency_id=agency_id_arg
    )
    assert response == expected_response
    
@pytest.mark.asyncio
async def test_update_delivery_ext_order_id(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    dto_arg = DeliveryAgencyUpdateConsignDTO(extOrderId="ext1", invoiceNumber="inv1", status="new")
    token_arg = "token1"
    agency_id_arg = "agency1"
    expected_response = "updated_ext_order_id"
    mock_agency_repository.update_delivery_ext_order_id.return_value = expected_response
    response = await agency_service.update_delivery_ext_order_id(dto=dto_arg, token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.update_delivery_ext_order_id.assert_called_once_with(
        dto=dto_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_return_delivery_flex(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    dto_arg = DeliveryInvoiceNumberDTO(invoiceNumber="inv_flex")
    token_arg = "token_flex"
    agency_id_arg = "agency_flex"
    expected_response = "flex_returned_successfully"
    mock_agency_repository.return_delivery_flex.return_value = expected_response
    response = await agency_service.return_delivery_flex(dto=dto_arg, token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.return_delivery_flex.assert_called_once_with(
        dto=dto_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_return_delivery_list_flex(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    dto_arg = DeliveryAgencyFlexListUpdateDTO(invoiceNumberList=["inv_flex1", "inv_flex2"])
    token_arg = "token_flex_list"
    agency_id_arg = "agency_flex_list"
    expected_response = "flex_list_returned_successfully"
    mock_agency_repository.return_delivery_list_flex.return_value = expected_response
    response = await agency_service.return_delivery_list_flex(dto=dto_arg, token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.return_delivery_list_flex.assert_called_once_with(
        dto=dto_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_find_delivery_list(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    delivery_dt_arg = "2023-01-01"
    token_arg = "token_find_list"
    agency_id_arg = "agency_find_list"
    expected_response = "delivery_list_data_found"
    mock_agency_repository.find_delivery_list.return_value = expected_response
    response = await agency_service.find_delivery_list(
        delivery_dt=delivery_dt_arg, token=token_arg, agency_id=agency_id_arg
    )
    mock_agency_repository.find_delivery_list.assert_called_once_with(
        delivery_dt=delivery_dt_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_update_delivery_state(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    dto_arg = DeliveryAgencyStateUpdateDTO(invoiceNumber="inv_state", status="DELIVERED")
    token_arg = "token_update_state"
    agency_id_arg = "agency_update_state"
    expected_response = "delivery_state_updated_successfully"
    mock_agency_repository.update_delivery_state.return_value = expected_response
    response = await agency_service.update_delivery_state(dto=dto_arg, token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.update_delivery_state.assert_called_once_with(
        dto=dto_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_find_delivery_by_invoice_list(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    invoice_list_arg = "inv1,inv2,inv3"
    token_arg = "token_find_invoices"
    agency_id_arg = "agency_find_invoices"
    expected_response = "invoice_data_list_found"
    mock_agency_repository.find_delivery_by_invoice_list.return_value = expected_response
    response = await agency_service.find_delivery_by_invoice_list(
        invoice_number_list=invoice_list_arg, token=token_arg, agency_id=agency_id_arg
    )
    mock_agency_repository.find_delivery_by_invoice_list.assert_called_once_with(
        invoice_number_list=invoice_list_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_save_postal_codes(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    postal_code_save_dto = PostalCodeSaveDTO(postNumber="12345", sido="서울", gugun="강남구", possibleArea="Y")
    dto_arg = PostalCodeListDTO(postNumberSaveList=[postal_code_save_dto], dawnDelivery="N")
    token_arg = "token_save_postal"
    agency_id_arg = "agency_save_postal"
    expected_response = "postal_codes_saved_successfully"
    mock_agency_repository.save_postal_codes.return_value = expected_response
    response = await agency_service.save_postal_codes(dto=dto_arg, token=token_arg, agency_id=agency_id_arg)
    mock_agency_repository.save_postal_codes.assert_called_once_with(
        dto=dto_arg, token=token_arg, agency_id=agency_id_arg
    )
    assert response == expected_response

@pytest.mark.asyncio
async def test_close_repository(agency_service: AgencyService, mock_agency_repository: AsyncMock):
    await agency_service.close_repository()
    mock_agency_repository.close.assert_called_once()
