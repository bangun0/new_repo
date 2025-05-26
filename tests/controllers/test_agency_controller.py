import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

# Import your FastAPI app instance and the service to be mocked
from app.main import app # app.main should contain your FastAPI instance
from app.services.agency_service import AgencyService
from app.schemas.agency_schemas import (
    AuthAgencyDTO, DeliveryAgencyUpdateConsignDTO, DeliveryInvoiceNumberDTO,
    DeliveryAgencyFlexListUpdateDTO, DeliveryAgencyStateUpdateDTO, PostalCodeListDTO,
    PostalCodeSaveDTO
)
# Import the actual controller to potentially override dependencies
from app.controllers import agency_controller 

# Mock for AgencyService
mock_agency_service = AsyncMock(spec=AgencyService)

# Dependency override function
def override_get_agency_service():
    return mock_agency_service

# Apply the override to the app for the agency_controller's dependency
# app.dependency_overrides[agency_controller.get_agency_service] = override_get_agency_service # Will be done in fixture

client = TestClient(app) # Create a TestClient instance

@pytest.fixture(autouse=True)
def reset_mocks_ensure_override(): # Renamed fixture
    global mock_agency_service # We are modifying the global mock_agency_service instance

    # Create a fresh mock instance for each test to ensure isolation
    mock_agency_service = AsyncMock(spec=AgencyService)
    
    # Apply the dependency override for this specific test run
    # This ensures the TestClient uses the exact mock instance we are configuring and asserting against
    original_override = app.dependency_overrides.get(agency_controller.get_agency_service)
    app.dependency_overrides[agency_controller.get_agency_service] = lambda: mock_agency_service
    
    # Configure default return values on the methods of the new mock
    mock_agency_service.check_auth.return_value = "auth_check_response_default"
    mock_agency_service.create_token.return_value = "token_creation_response_default"
    mock_agency_service.update_delivery_ext_order_id.return_value = "put_response_default"
    mock_agency_service.return_delivery_flex.return_value = "put_flex_response_default"
    mock_agency_service.return_delivery_list_flex.return_value = "put_list_flex_response_default"
    mock_agency_service.find_delivery_list.return_value = "post_find_list_response_default"
    mock_agency_service.update_delivery_state.return_value = "put_state_response_default"
    mock_agency_service.find_delivery_by_invoice_list.return_value = "post_find_invoices_response_default"
    mock_agency_service.save_postal_codes.return_value = "post_save_postal_response_default"

    yield # Test runs here

    # Clean up: restore original override or clear if none was there
    if original_override:
        app.dependency_overrides[agency_controller.get_agency_service] = original_override
    else:
        del app.dependency_overrides[agency_controller.get_agency_service]


def test_check_auth_endpoint_success():
    expected_response_data = "auth_check_controller_response"
    mock_agency_service.check_auth.return_value = expected_response_data
    
    auth_token = "test_auth_token"
    agency_id_header = "test_agency_id"

    response = client.post(
        "/api/agency/auth",
        headers={"Authorization": auth_token, "agencyId": agency_id_header}
    )
    
    assert response.status_code == 200
    assert response.json() == expected_response_data 
    mock_agency_service.check_auth.assert_called_once_with(token=auth_token, agency_id=agency_id_header)

def test_create_token_endpoint_success():
    expected_response_data = "token_create_controller_response"
    mock_agency_service.create_token.return_value = expected_response_data

    auth_dto_payload = {"accessKey": "ak", "nonce": "nn", "timestamp": "ts"}
    auth_token_header = "auth_for_token_creation"
    agency_id_header = "agency_for_token_creation"

    response = client.post(
        "/api/agency/auth/token",
        headers={"Authorization": auth_token_header, "agencyId": agency_id_header},
        json=auth_dto_payload
    )

    if response.status_code == 422:
        print("DEBUG 422 Response for test_create_token_endpoint_success:", response.json())
    assert response.status_code == 200
    assert response.json() == expected_response_data
    # Arguments are passed as keyword args, so they are in call_args[1]
    assert mock_agency_service.create_token.call_count == 1 # Ensure it was called
    called_kwargs = mock_agency_service.create_token.call_args[1]
    called_with_dto = called_kwargs['auth_dto']
    
    assert isinstance(called_with_dto, AuthAgencyDTO)
    assert called_with_dto.accessKey == auth_dto_payload["accessKey"]
    
    mock_agency_service.create_token.assert_called_once_with(
        auth_dto=called_with_dto,
        authorization_header=auth_token_header,
        agency_id=agency_id_header
    )

def test_update_delivery_ext_order_id_endpoint():
    expected_response_data = "delivery_updated_controller"
    mock_agency_service.update_delivery_ext_order_id.return_value = expected_response_data

    dto_payload = {"extOrderId": "ext123", "invoiceNumber": "inv789", "status": "done"}
    auth_token = "token_put_delivery"
    agency_id = "agency_put_delivery"

    response = client.put(
        "/api/agency/delivery",
        headers={"Authorization": auth_token, "agencyId": agency_id},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    
    assert mock_agency_service.update_delivery_ext_order_id.call_count == 1
    called_kwargs = mock_agency_service.update_delivery_ext_order_id.call_args[1]
    called_with_dto = called_kwargs['dto']
    
    assert isinstance(called_with_dto, DeliveryAgencyUpdateConsignDTO)
    assert called_with_dto.invoiceNumber == dto_payload["invoiceNumber"]
    mock_agency_service.update_delivery_ext_order_id.assert_called_once_with(
        dto=called_with_dto, token=auth_token, agency_id=agency_id
    )
    
def test_find_delivery_list_endpoint():
    expected_response_data = "delivery_list_found_controller"
    mock_agency_service.find_delivery_list.return_value = expected_response_data

    delivery_dt_path = "2023-11-01"
    auth_token = "token_find_list"
    agency_id = "agency_find_list"

    response = client.post(
        f"/api/agency/delivery/list/{delivery_dt_path}",
        headers={"Authorization": auth_token, "agencyId": agency_id}
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    mock_agency_service.find_delivery_list.assert_called_once_with(
        delivery_dt=delivery_dt_path, token=auth_token, agency_id=agency_id
    )

# --- Completed tests for remaining endpoints ---

def test_return_delivery_flex_endpoint():
    expected_response_data = "delivery_flex_returned_controller"
    mock_agency_service.return_delivery_flex.return_value = expected_response_data

    dto_payload = {"invoiceNumber": "inv_flex_test"}
    auth_token = "token_flex_put"
    agency_id = "agency_flex_put"

    response = client.put(
        "/api/agency/delivery/flex",
        headers={"Authorization": auth_token, "agencyId": agency_id},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    
    assert mock_agency_service.return_delivery_flex.call_count == 1
    called_kwargs = mock_agency_service.return_delivery_flex.call_args[1]
    called_with_dto = called_kwargs['dto']
        
    assert isinstance(called_with_dto, DeliveryInvoiceNumberDTO)
    assert called_with_dto.invoiceNumber == dto_payload["invoiceNumber"]
    mock_agency_service.return_delivery_flex.assert_called_once_with(
        dto=called_with_dto, token=auth_token, agency_id=agency_id
    )

def test_return_delivery_list_flex_endpoint():
    expected_response_data = "delivery_list_flex_returned_controller"
    mock_agency_service.return_delivery_list_flex.return_value = expected_response_data

    dto_payload = {"invoiceNumberList": ["inv_flex1", "inv_flex2"]}
    auth_token = "token_list_flex_put"
    agency_id = "agency_list_flex_put"

    response = client.put(
        "/api/agency/delivery/list/flex",
        headers={"Authorization": auth_token, "agencyId": agency_id},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    
    assert mock_agency_service.return_delivery_list_flex.call_count == 1
    called_kwargs = mock_agency_service.return_delivery_list_flex.call_args[1]
    called_with_dto = called_kwargs['dto']
        
    assert isinstance(called_with_dto, DeliveryAgencyFlexListUpdateDTO)
    assert called_with_dto.invoiceNumberList == dto_payload["invoiceNumberList"]
    mock_agency_service.return_delivery_list_flex.assert_called_once_with(
        dto=called_with_dto, token=auth_token, agency_id=agency_id
    )

def test_update_delivery_state_endpoint():
    expected_response_data = "delivery_state_updated_controller"
    mock_agency_service.update_delivery_state.return_value = expected_response_data

    dto_payload = {"invoiceNumber": "inv_state_test", "status": "DELIVERED", "holdCode": "H01", "imgUrl": "http://example.com/image.jpg"}
    auth_token = "token_state_put"
    agency_id = "agency_state_put"

    response = client.put(
        "/api/agency/delivery/state",
        headers={"Authorization": auth_token, "agencyId": agency_id},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    
    assert mock_agency_service.update_delivery_state.call_count == 1
    called_kwargs = mock_agency_service.update_delivery_state.call_args[1]
    called_with_dto = called_kwargs['dto']
        
    assert isinstance(called_with_dto, DeliveryAgencyStateUpdateDTO)
    assert called_with_dto.invoiceNumber == dto_payload["invoiceNumber"]
    assert called_with_dto.status == dto_payload["status"]
    mock_agency_service.update_delivery_state.assert_called_once_with(
        dto=called_with_dto, token=auth_token, agency_id=agency_id
    )

def test_find_delivery_by_invoice_list_endpoint():
    expected_response_data = "delivery_by_invoices_found_controller"
    mock_agency_service.find_delivery_by_invoice_list.return_value = expected_response_data

    invoice_number_list_path = "inv1,inv2,inv3"
    auth_token = "token_find_by_invoices"
    agency_id = "agency_find_by_invoices"

    response = client.post(
        f"/api/agency/delivery/{invoice_number_list_path}",
        headers={"Authorization": auth_token, "agencyId": agency_id}
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    mock_agency_service.find_delivery_by_invoice_list.assert_called_once_with(
        invoice_number_list=invoice_number_list_path, token=auth_token, agency_id=agency_id
    )

def test_save_postal_codes_endpoint():
    expected_response_data = "postal_codes_saved_controller"
    mock_agency_service.save_postal_codes.return_value = expected_response_data

    postal_save_item = {"postNumber": "12345", "sido": "서울", "gugun": "강남구", "possibleArea": "Y"}
    dto_payload = {"postNumberSaveList": [postal_save_item], "dawnDelivery": "N"}
    auth_token = "token_save_postal"
    agency_id = "agency_save_postal"

    response = client.post(
        "/api/agency/postal/save",
        headers={"Authorization": auth_token, "agencyId": agency_id},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_response_data
    
    assert mock_agency_service.save_postal_codes.call_count == 1
    called_kwargs = mock_agency_service.save_postal_codes.call_args[1]
    called_with_dto = called_kwargs['dto']
        
    assert isinstance(called_with_dto, PostalCodeListDTO)
    assert len(called_with_dto.postNumberSaveList) == 1
    assert called_with_dto.postNumberSaveList[0].postNumber == postal_save_item["postNumber"]
    mock_agency_service.save_postal_codes.assert_called_once_with(
        dto=called_with_dto, token=auth_token, agency_id=agency_id
    )
