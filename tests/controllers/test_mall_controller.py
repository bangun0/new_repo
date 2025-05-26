import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app # FastAPI app instance
from app.services.mall_service import MallService
from app.schemas.mall_schemas import (
    GoodsReturnRequestDTO, MallApiDeliveryDTO, GoodsDTO,
    MallApiReturnDTO, GoodsNoDawnDTO
)
from app.controllers import mall_controller # To override its dependency

# Mock for MallService
mock_mall_service = AsyncMock(spec=MallService)

# Dependency override function for MallService
def override_get_mall_service():
    return mock_mall_service

# Apply the override for mall_controller's dependency
# app.dependency_overrides[mall_controller.get_mall_service] = override_get_mall_service # Will be done in fixture

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_mall_mocks_ensure_override(): # Renamed fixture
    global mock_mall_service # We are modifying the global mock_mall_service instance

    # Create a fresh mock instance for each test to ensure isolation
    mock_mall_service = AsyncMock(spec=MallService)
    
    # Apply the dependency override for this specific test run
    original_override = app.dependency_overrides.get(mall_controller.get_mall_service)
    app.dependency_overrides[mall_controller.get_mall_service] = lambda: mock_mall_service
    
    # Configure default return values on the methods of the new mock
    mock_mall_service.cancel_delivery.return_value = "cancel_delivery_response_default"
    mock_mall_service.find_by_invoice.return_value = "find_invoice_response_default"
    mock_mall_service.find_by_invoice_list.return_value = "find_invoice_list_response_default"
    mock_mall_service.delivery_list_register.return_value = "delivery_list_reg_response_default"
    mock_mall_service.delivery_register.return_value = "delivery_reg_response_default"
    mock_mall_service.possible_delivery.return_value = "possible_delivery_check_response_default"
    mock_mall_service.return_delivery.return_value = "return_delivery_response_default"
    mock_mall_service.return_list_register.return_value = "return_list_reg_response_default"
    mock_mall_service.return_register.return_value = "return_reg_response_default"

    yield # Test runs here

    # Clean up: restore original override or clear if none was there
    if original_override:
        app.dependency_overrides[mall_controller.get_mall_service] = original_override
    else:
        del app.dependency_overrides[mall_controller.get_mall_service]


def test_cancel_delivery_endpoint():
    expected_data = "mall_cancel_success"
    mock_mall_service.cancel_delivery.return_value = expected_data
    
    dto_payload = {"invoiceNumber": "INV_CANCEL_001"}
    auth_token = "mall_auth_token_cancel"

    response = client.post(
        "/api/mall/cancelDelivery",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.cancel_delivery.call_count == 1
    called_kwargs = mock_mall_service.cancel_delivery.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, GoodsReturnRequestDTO)
    assert called_dto.invoiceNumber == dto_payload["invoiceNumber"]
    mock_mall_service.cancel_delivery.assert_called_once_with(dto=called_dto, token=auth_token)

def test_find_by_invoice_endpoint():
    expected_data = "mall_invoice_data_found"
    mock_mall_service.find_by_invoice.return_value = expected_data
    
    invoice_num_path = "INV007"
    auth_token = "mall_auth_token_find_inv"

    response = client.get(
        f"/api/mall/delivery/{invoice_num_path}",
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_mall_service.find_by_invoice.assert_called_once_with(invoice_number=invoice_num_path, token=auth_token)

def test_possible_delivery_endpoint():
    expected_data = "mall_possible_delivery_yes"
    mock_mall_service.possible_delivery.return_value = expected_data

    auth_token = "mall_auth_token_possible"
    query_params = {"address": "123 Main St", "postalCode": "90210", "dawnDelivery": "Y"}

    response = client.get(
        "/api/mall/possibleDelivery",
        headers={"Authorization": auth_token},
        params=query_params
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_mall_service.possible_delivery.assert_called_once_with(
        address=query_params["address"],
        token=auth_token,
        postal_code=query_params["postalCode"],
        dawn_delivery=query_params["dawnDelivery"]
    )
    
def test_possible_delivery_endpoint_minimal_params():
    expected_data = "mall_possible_delivery_minimal_check"
    mock_mall_service.possible_delivery.return_value = expected_data

    auth_token = "mall_auth_token_minimal_possible"
    query_params = {"address": "456 Side St"}

    response = client.get(
        "/api/mall/possibleDelivery",
        headers={"Authorization": auth_token},
        params=query_params
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_mall_service.possible_delivery.assert_called_once_with(
        address=query_params["address"],
        token=auth_token,
        postal_code=None, # Optional params default to None
        dawn_delivery=None
    )

# --- Completed tests for remaining endpoints ---

def test_find_by_invoice_list_endpoint():
    expected_data = "mall_invoice_list_data"
    mock_mall_service.find_by_invoice_list.return_value = expected_data
    
    invoice_list_path = "INV001,INV002"
    auth_token = "mall_auth_token_find_list"

    response = client.get(
        f"/api/mall/deliveryList/{invoice_list_path}",
        headers={"Authorization": auth_token}
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    mock_mall_service.find_by_invoice_list.assert_called_once_with(
        invoice_number_list=invoice_list_path, token=auth_token
    )

def test_delivery_list_register_endpoint():
    expected_data = "mall_delivery_list_registered"
    mock_mall_service.delivery_list_register.return_value = expected_data

    goods_item_payload = {
        "deliveryAddress": "123 Deliver St", "deliveryName": "John D.",
        "deliveryPhone": "555-0101", "mallName": "QuickMall"
    }
    dto_payload = {
        "goodsList": [goods_item_payload],
        "dawnDelivery": "N" 
    }
    auth_token = "mall_auth_token_dlr"

    response = client.post(
        "/api/mall/deliveryListRegister",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.delivery_list_register.call_count == 1
    called_kwargs = mock_mall_service.delivery_list_register.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, MallApiDeliveryDTO)
    assert len(called_dto.goodsList) == 1
    assert called_dto.goodsList[0].deliveryName == goods_item_payload["deliveryName"]
    assert called_dto.dawnDelivery == dto_payload["dawnDelivery"]
    mock_mall_service.delivery_list_register.assert_called_once_with(
        dto=called_dto, token=auth_token
    )

def test_delivery_register_endpoint():
    expected_data = "mall_delivery_registered"
    mock_mall_service.delivery_register.return_value = expected_data

    dto_payload = {
        "deliveryAddress": "456 Single Deliver St", "deliveryName": "Jane S.",
        "deliveryPhone": "555-0202", "mallName": "SoloMall", "dawnDelivery": "Y",
        "goodsName": "Big Box", "quantity": 1
    }
    auth_token = "mall_auth_token_dr"

    response = client.post(
        "/api/mall/deliveryRegister",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.delivery_register.call_count == 1
    called_kwargs = mock_mall_service.delivery_register.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, GoodsDTO)
    assert called_dto.deliveryName == dto_payload["deliveryName"]
    assert called_dto.dawnDelivery == dto_payload["dawnDelivery"]
    assert called_dto.goodsName == dto_payload["goodsName"]
    mock_mall_service.delivery_register.assert_called_once_with(
        dto=called_dto, token=auth_token
    )

def test_return_delivery_endpoint():
    expected_data = "mall_return_delivery_requested"
    mock_mall_service.return_delivery.return_value = expected_data

    dto_payload = {"invoiceNumber": "INV_RETURN_00X"}
    auth_token = "mall_auth_token_return_del"

    response = client.post(
        "/api/mall/returnDelivery",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.return_delivery.call_count == 1
    called_kwargs = mock_mall_service.return_delivery.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, GoodsReturnRequestDTO)
    assert called_dto.invoiceNumber == dto_payload["invoiceNumber"]
    mock_mall_service.return_delivery.assert_called_once_with(
        dto=called_dto, token=auth_token
    )

def test_return_list_register_endpoint():
    expected_data = "mall_return_list_registered"
    mock_mall_service.return_list_register.return_value = expected_data

    goods_item_payload = {
        "deliveryAddress": "789 Return St", "deliveryName": "Robert R.",
        "deliveryPhone": "555-0303", "mallName": "ReturnEmporium"
    }
    # MallApiReturnDTO uses GoodsNoDawnDTO for its goodsList
    dto_payload = {"goodsList": [goods_item_payload]}
    auth_token = "mall_auth_token_rlr"

    response = client.post(
        "/api/mall/returnListRegister",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.return_list_register.call_count == 1
    called_kwargs = mock_mall_service.return_list_register.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, MallApiReturnDTO)
    assert len(called_dto.goodsList) == 1
    assert called_dto.goodsList[0].deliveryName == goods_item_payload["deliveryName"]
    mock_mall_service.return_list_register.assert_called_once_with(
        dto=called_dto, token=auth_token
    )

def test_return_register_endpoint():
    expected_data = "mall_return_registered"
    mock_mall_service.return_register.return_value = expected_data

    dto_payload = {
        "deliveryAddress": "101 Single Return St", "deliveryName": "Susan S.",
        "deliveryPhone": "555-0404", "mallName": "OneReturn",
        "goodsName": "Small Item", "quantity": 3
    }
    auth_token = "mall_auth_token_rr"

    response = client.post(
        "/api/mall/returnRegister",
        headers={"Authorization": auth_token},
        json=dto_payload
    )
    assert response.status_code == 200
    assert response.json() == expected_data
    
    assert mock_mall_service.return_register.call_count == 1
    called_kwargs = mock_mall_service.return_register.call_args[1]
    called_dto = called_kwargs['dto']
        
    assert isinstance(called_dto, GoodsNoDawnDTO)
    assert called_dto.deliveryName == dto_payload["deliveryName"]
    assert called_dto.goodsName == dto_payload["goodsName"]
    mock_mall_service.return_register.assert_called_once_with(
        dto=called_dto, token=auth_token
    )
