"""
pytest 설정 파일
테스트에 필요한 공통 fixtures를 정의합니다.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import Response
import json

from app.models.base import AuthInfo
from app.schemas.mall import DeliveryAddressSchema, DeliveryItemSchema, SingleDeliveryRegisterRequest


@pytest.fixture
def mock_auth_info():
    """
    테스트용 인증 정보 fixture
    
    Returns:
        AuthInfo: 테스트용 인증 정보
    """
    return AuthInfo(
        agency_id="test_agency_123",
        auth_token="Bearer test_token_abc123"
    )


@pytest.fixture
def mock_delivery_address():
    """
    테스트용 배송 주소 fixture
    
    Returns:
        DeliveryAddressSchema: 테스트용 배송 주소
    """
    return DeliveryAddressSchema(
        zipcode="12345",
        address="서울시 강남구 테헤란로 123",
        address_detail="456호",
        receiver_name="홍길동",
        receiver_phone="010-1234-5678",
        receiver_phone2="02-1234-5678",
        memo="문 앞에 놓아주세요"
    )


@pytest.fixture
def mock_delivery_item():
    """
    테스트용 배송 상품 fixture
    
    Returns:
        DeliveryItemSchema: 테스트용 배송 상품
    """
    return DeliveryItemSchema(
        item_name="테스트 상품",
        quantity=2,
        price=10000,
        item_code="ITEM001",
        option="사이즈: M, 색상: 블루"
    )


@pytest.fixture
def mock_delivery_request(mock_delivery_address, mock_delivery_item):
    """
    테스트용 배송 등록 요청 fixture
    
    Args:
        mock_delivery_address: 테스트용 배송 주소
        mock_delivery_item: 테스트용 배송 상품
        
    Returns:
        SingleDeliveryRegisterRequest: 테스트용 배송 등록 요청
    """
    return SingleDeliveryRegisterRequest(
        mall_order_number="ORDER123456",
        delivery_date="2024-12-31",
        address=mock_delivery_address,
        items=[mock_delivery_item],
        delivery_fee=3000,
        cod_amount=0
    )


@pytest.fixture
def mock_http_response():
    """
    테스트용 HTTP 응답 fixture
    
    Returns:
        MagicMock: Mock HTTP 응답 객체
    """
    def create_response(status_code=200, json_data=None):
        response = MagicMock(spec=Response)
        response.status_code = status_code
        response.json.return_value = json_data or {"success": True, "message": "Test successful"}
        response.raise_for_status = MagicMock()
        return response
    
    return create_response


@pytest.fixture
def mock_http_client():
    """
    테스트용 HTTP 클라이언트 fixture
    
    Returns:
        AsyncMock: Mock HTTP 클라이언트
    """
    client = AsyncMock()
    
    # 기본 성공 응답 설정
    success_response = MagicMock(spec=Response)
    success_response.status_code = 200
    success_response.json.return_value = {"success": True, "message": "Test successful"}
    success_response.raise_for_status = MagicMock()
    
    client.get.return_value = success_response
    client.post.return_value = success_response
    client.put.return_value = success_response
    client.delete.return_value = success_response
    
    return client


@pytest.fixture
def mock_repository():
    """
    테스트용 Repository fixture
    
    Returns:
        AsyncMock: Mock Repository 객체
    """
    repository = AsyncMock()
    
    # 기본 응답 설정
    repository.health_check.return_value = True
    repository.generate_token.return_value = {
        "access_token": "test_token",
        "token_type": "Bearer",
        "expires_in": 3600
    }
    repository.validate_token.return_value = {
        "is_valid": True,
        "expires_at": "2024-12-31T23:59:59",
        "agency_id": "test_agency_123"
    }
    repository.register_single_delivery.return_value = {
        "invoice_number": "INV123456789",
        "mall_order_number": "ORDER123456",
        "registered_at": "2024-01-01T00:00:00"
    }
    repository.track_delivery.return_value = {
        "invoice_number": "INV123456789",
        "current_status": "in_transit",
        "tracking_history": []
    }
    
    return repository


@pytest.fixture
def mock_service():
    """
    테스트용 Service fixture
    
    Returns:
        AsyncMock: Mock Service 객체
    """
    service = AsyncMock()
    
    # 기본 성공 응답 설정
    service.health_check.return_value = {
        "success": True,
        "message": "Service is healthy",
        "data": {"is_healthy": True}
    }
    service.generate_authentication_token.return_value = {
        "success": True,
        "message": "Token generated successfully",
        "data": {
            "access_token": "test_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
    }
    service.register_single_delivery.return_value = {
        "success": True,
        "message": "Delivery registered successfully",
        "data": {
            "invoice_number": "INV123456789",
            "mall_order_number": "ORDER123456"
        }
    }
    
    return service


@pytest.fixture(autouse=True)
def reset_mocks():
    """
    각 테스트 실행 전에 mock 객체들을 초기화합니다.
    """
    yield
    # 테스트 후 정리 작업이 필요한 경우 여기에 추가