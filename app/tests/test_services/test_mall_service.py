"""
MallService 단위 테스트
쇼핑몰 Service의 기능을 테스트합니다.
"""
import pytest
from unittest.mock import AsyncMock, patch

from app.services.mall_service import MallService
from app.models.base import AuthInfo
from app.schemas.mall import (
    SingleDeliveryRegisterRequest,
    MultipleDeliveryRegisterRequest,
    DeliveryAvailabilityRequest,
    DeliveryCancelRequest,
    DeliveryReturnRequest
)


class TestMallService:
    """MallService 테스트 클래스"""
    
    @pytest.fixture
    def service(self):
        """MallService 인스턴스 생성"""
        return MallService()
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, service, mock_repository):
        """헬스체크 성공 테스트"""
        # Given
        mock_repository.health_check.return_value = True
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.health_check()
            
            # Then
            assert result["success"] is True
            assert result["data"]["is_healthy"] is True
            mock_repository.health_check.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, service):
        """헬스체크 실패 테스트"""
        # Given
        mock_repository = AsyncMock()
        mock_repository.health_check.side_effect = Exception("Repository error")
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.health_check()
            
            # Then
            assert result["success"] is False
            assert "SERVICE_ERROR" in result["error_code"]
    
    @pytest.mark.asyncio
    async def test_register_single_delivery_success(self, service, mock_repository, mock_delivery_request, mock_auth_info):
        """단일 배송 등록 성공 테스트"""
        # Given
        expected_response = {
            "invoice_number": "INV123456789",
            "mall_order_number": "ORDER123456",
            "registered_at": "2024-01-01T00:00:00"
        }
        mock_repository.register_single_delivery.return_value = expected_response
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.register_single_delivery(mock_delivery_request, mock_auth_info)
            
            # Then
            assert result["success"] is True
            assert result["data"] == expected_response
            mock_repository.register_single_delivery.assert_called_once_with(mock_delivery_request, mock_auth_info)
    
    @pytest.mark.asyncio
    async def test_register_single_delivery_invalid_auth(self, service, mock_delivery_request):
        """단일 배송 등록 - 잘못된 인증 정보 테스트"""
        # Given
        invalid_auth = AuthInfo(agency_id="", auth_token="")
        
        # When
        result = await service.register_single_delivery(mock_delivery_request, invalid_auth)
        
        # Then
        assert result["success"] is False
        assert result["error_code"] == "INVALID_AUTH"
    
    @pytest.mark.asyncio
    async def test_register_multiple_deliveries_success(self, service, mock_repository, mock_delivery_request, mock_auth_info):
        """다중 배송 등록 성공 테스트"""
        # Given
        multiple_request = MultipleDeliveryRegisterRequest(deliveries=[mock_delivery_request])
        expected_response = {
            "registered_deliveries": [{"invoice_number": "INV123456789"}],
            "total_requested": 1,
            "total_success": 1,
            "total_failed": 0
        }
        mock_repository.register_multiple_deliveries.return_value = expected_response
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.register_multiple_deliveries(multiple_request, mock_auth_info)
            
            # Then
            assert result["success"] is True
            assert result["data"] == expected_response
            mock_repository.register_multiple_deliveries.assert_called_once_with(multiple_request, mock_auth_info)
    
    @pytest.mark.asyncio
    async def test_register_multiple_deliveries_empty_list(self, service, mock_auth_info):
        """다중 배송 등록 - 빈 배송 목록 테스트"""
        # Given
        empty_request = MultipleDeliveryRegisterRequest(deliveries=[])
        
        # When
        result = await service.register_multiple_deliveries(empty_request, mock_auth_info)
        
        # Then
        assert result["success"] is False
        assert result["error_code"] == "EMPTY_DELIVERY_LIST"
    
    @pytest.mark.asyncio
    async def test_register_multiple_deliveries_too_many(self, service, mock_delivery_request, mock_auth_info):
        """다중 배송 등록 - 너무 많은 배송 테스트"""
        # Given
        # Pydantic이 이미 validation error를 발생시키므로, 
        # 이 경우는 service level에서 체크하는 것이 아니라 schema level에서 처리됨
        # 서비스 레벨에서 체크하도록 변경
        deliveries_list = [mock_delivery_request] * 101
        
        # When & Then - Pydantic validation error가 발생할 것임
        with pytest.raises(Exception):  # ValidationError 예상
            MultipleDeliveryRegisterRequest(deliveries=deliveries_list)
    
    @pytest.mark.asyncio
    async def test_track_delivery_status_success(self, service, mock_repository, mock_auth_info):
        """배송 추적 성공 테스트"""
        # Given
        invoice_number = "INV123456789"
        expected_response = {
            "invoice_number": "INV123456789",
            "current_status": "in_transit",
            "tracking_history": []
        }
        mock_repository.track_delivery.return_value = expected_response
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.track_delivery_status(invoice_number, mock_auth_info)
            
            # Then
            assert result["success"] is True
            assert result["data"] == expected_response
            mock_repository.track_delivery.assert_called_once_with(invoice_number, mock_auth_info)
    
    @pytest.mark.asyncio
    async def test_track_delivery_status_empty_invoice(self, service, mock_auth_info):
        """배송 추적 - 빈 송장번호 테스트"""
        # Given
        empty_invoice = ""
        
        # When
        result = await service.track_delivery_status(empty_invoice, mock_auth_info)
        
        # Then
        assert result["success"] is False
        assert result["error_code"] == "INVALID_INPUT"
    
    @pytest.mark.asyncio
    async def test_check_delivery_availability_success(self, service, mock_repository, mock_auth_info):
        """배송 가능 여부 확인 성공 테스트"""
        # Given
        zipcode = "12345"
        delivery_date = "2024-01-01"
        expected_response = {
            "zipcode": "12345",
            "is_deliverable": True,
            "delivery_fee": 3000
        }
        mock_repository.check_delivery_availability.return_value = expected_response
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.check_delivery_availability(zipcode, delivery_date, mock_auth_info)
            
            # Then
            assert result["success"] is True
            assert result["data"] == expected_response
    
    @pytest.mark.asyncio
    async def test_check_delivery_availability_invalid_date(self, service, mock_auth_info):
        """배송 가능 여부 확인 - 잘못된 날짜 형식 테스트"""
        # Given
        zipcode = "12345"
        invalid_date = "2024/01/01"  # 잘못된 형식
        
        # When
        result = await service.check_delivery_availability(zipcode, invalid_date, mock_auth_info)
        
        # Then
        assert result["success"] is False
        assert result["error_code"] == "INVALID_DATE_FORMAT"
    
    @pytest.mark.asyncio
    async def test_cancel_delivery_success(self, service, mock_repository, mock_auth_info):
        """배송 취소 성공 테스트"""
        # Given
        invoice_number = "INV123456789"
        cancel_reason = "고객 요청"
        expected_response = {
            "invoice_number": "INV123456789",
            "cancelled_at": "2024-01-01T00:00:00",
            "cancel_reason": "고객 요청"
        }
        mock_repository.cancel_delivery.return_value = expected_response
        
        with patch.object(service, 'repository', mock_repository):
            # When
            result = await service.cancel_delivery(invoice_number, cancel_reason, mock_auth_info)
            
            # Then
            assert result["success"] is True
            assert result["data"] == expected_response
    
    @pytest.mark.asyncio
    async def test_cancel_delivery_missing_reason(self, service, mock_auth_info):
        """배송 취소 - 취소 사유 누락 테스트"""
        # Given
        invoice_number = "INV123456789"
        cancel_reason = ""  # 빈 사유
        
        # When
        result = await service.cancel_delivery(invoice_number, cancel_reason, mock_auth_info)
        
        # Then
        assert result["success"] is False
        assert result["error_code"] == "INVALID_INPUT"
    
    @pytest.mark.asyncio
    async def test_validate_delivery_request_missing_items(self, service):
        """배송 요청 검증 - 상품 누락 테스트"""
        # Given
        from app.schemas.mall import DeliveryAddressSchema
        
        invalid_request = SingleDeliveryRegisterRequest(
            mall_order_number="ORDER123456",
            delivery_date="2024-01-01",
            address=DeliveryAddressSchema(
                zipcode="12345",
                address="서울시 강남구",
                address_detail="123호",
                receiver_name="홍길동",
                receiver_phone="010-1234-5678"
            ),
            items=[]  # 빈 상품 목록
        )
        
        # When
        result = service._validate_delivery_request(invalid_request)
        
        # Then
        assert result["is_valid"] is False
        assert "At least one item is required" in result["message"]
    
    @pytest.mark.asyncio
    async def test_validate_delivery_request_invalid_item(self, service, mock_delivery_address):
        """배송 요청 검증 - 잘못된 상품 정보 테스트"""
        # Given
        from app.schemas.mall import DeliveryItemSchema
        
        # Pydantic validation을 우회하여 직접 생성 (내부 검증 로직 테스트용)
        # 유효한 아이템을 먼저 생성하고 수동으로 값 변경
        valid_item = DeliveryItemSchema(
            item_name="테스트 상품",
            quantity=1,
            price=100
        )
        
        # 유효한 요청 생성 후 내부 검증 로직 테스트
        valid_request = SingleDeliveryRegisterRequest(
            mall_order_number="ORDER123456",
            delivery_date="2024-01-01",
            address=mock_delivery_address,
            items=[valid_item]
        )
        
        # 아이템의 값을 강제로 변경하여 검증 로직 테스트
        valid_request.items[0].item_name = ""
        valid_request.items[0].quantity = 0
        valid_request.items[0].price = -100
        
        # When
        result = service._validate_delivery_request(valid_request)
        
        # Then
        assert result["is_valid"] is False
        assert "Invalid item information" in result["message"]