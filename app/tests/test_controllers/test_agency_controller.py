"""
AgencyController 단위 테스트
대리점 Controller의 기능을 테스트합니다.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from app.controllers.agency_controller import agency_service


class TestAgencyController:
    """AgencyController 테스트 클래스"""
    
    @pytest.fixture
    def client(self):
        """TestClient 인스턴스 생성"""
        return TestClient(app)
    
    @pytest.fixture
    def auth_headers(self):
        """테스트용 인증 헤더"""
        return {
            "Authorization": "Bearer test_token",
            "AgencyId": "test_agency_123"
        }
    
    def test_health_check_success(self, client):
        """헬스체크 성공 테스트"""
        # Given
        mock_service = AsyncMock()
        mock_service.health_check.return_value = {
            "success": True,
            "message": "Service is healthy",
            "data": {"is_healthy": True}
        }
        
        with patch.object(agency_service, 'health_check', mock_service.health_check):
            # When
            response = client.get("/api/v1/agency/health")
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["is_healthy"] is True
    
    def test_generate_token_success(self, client):
        """토큰 생성 성공 테스트"""
        # Given
        request_data = {
            "agency_id": "test_agency_123",
            "api_key": "test_api_key"
        }
        
        mock_service = AsyncMock()
        mock_service.generate_authentication_token.return_value = {
            "success": True,
            "message": "Token generated successfully",
            "data": {
                "access_token": "new_token",
                "token_type": "Bearer",
                "expires_in": 3600
            }
        }
        
        with patch.object(agency_service, 'generate_authentication_token', mock_service.generate_authentication_token):
            # When
            response = client.post("/api/v1/agency/auth/token", json=request_data)
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "access_token" in data["data"]
    
    def test_generate_token_failure(self, client):
        """토큰 생성 실패 테스트"""
        # Given
        request_data = {
            "agency_id": "",  # 빈 agency_id
            "api_key": "test_api_key"
        }
        
        mock_service = AsyncMock()
        mock_service.generate_authentication_token.return_value = {
            "success": False,
            "message": "Agency ID and API key are required",
            "error_code": "INVALID_INPUT",
            "data": None
        }
        
        with patch.object(agency_service, 'generate_authentication_token', mock_service.generate_authentication_token):
            # When
            response = client.post("/api/v1/agency/auth/token", json=request_data)
            
            # Then
            assert response.status_code == 400
            data = response.json()
            assert "INVALID_INPUT" in data["detail"]["error_code"]
    
    def test_validate_token_success(self, client, auth_headers):
        """토큰 검증 성공 테스트"""
        # Given
        request_data = {"token": "test_token_to_validate"}
        
        mock_service = AsyncMock()
        mock_service.validate_authentication_token.return_value = {
            "success": True,
            "message": "Token is valid",
            "data": {
                "is_valid": True,
                "expires_at": "2024-12-31T23:59:59",
                "agency_id": "test_agency_123"
            }
        }
        
        with patch.object(agency_service, 'validate_authentication_token', mock_service.validate_authentication_token):
            # When
            response = client.post(
                "/api/v1/agency/auth",
                json=request_data,
                headers=auth_headers
            )
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["is_valid"] is True
    
    def test_validate_token_missing_headers(self, client):
        """토큰 검증 - 헤더 누락 테스트"""
        # Given
        request_data = {"token": "test_token_to_validate"}
        
        # When (헤더 없이 요청)
        response = client.post("/api/v1/agency/auth", json=request_data)
        
        # Then
        assert response.status_code == 422  # Validation error
    
    def test_assign_delivery_success(self, client, auth_headers):
        """배송 배정 성공 테스트"""
        # Given
        request_data = {
            "invoice_number": "INV123456789",
            "driver_name": "홍길동",
            "driver_phone": "010-1234-5678",
            "estimated_delivery_time": "14:00"
        }
        
        mock_service = AsyncMock()
        mock_service.assign_delivery_to_driver.return_value = {
            "success": True,
            "message": "Delivery assigned successfully",
            "data": {
                "invoice_number": "INV123456789",
                "assigned_at": "2024-01-01T00:00:00"
            }
        }
        
        with patch.object(agency_service, 'assign_delivery_to_driver', mock_service.assign_delivery_to_driver):
            # When
            response = client.put(
                "/api/v1/agency/delivery",
                json=request_data,
                headers=auth_headers
            )
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["invoice_number"] == "INV123456789"
    
    def test_get_delivery_list_success(self, client, auth_headers):
        """배송 목록 조회 성공 테스트"""
        # Given
        delivery_date = "2024-01-01"
        
        mock_service = AsyncMock()
        mock_service.get_delivery_information_list.return_value = {
            "success": True,
            "message": "Delivery list retrieved successfully",
            "data": {
                "deliveries": [],
                "total_count": 0,
                "page": 1,
                "total_pages": 0
            }
        }
        
        with patch.object(agency_service, 'get_delivery_information_list', mock_service.get_delivery_information_list):
            # When
            response = client.post(
                f"/api/v1/agency/delivery/list/{delivery_date}",
                headers=auth_headers,
                params={"page": 1, "size": 10}
            )
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "deliveries" in data["data"]
    
    def test_get_delivery_list_with_filters(self, client, auth_headers):
        """배송 목록 조회 - 필터 적용 테스트"""
        # Given
        delivery_date = "2024-01-01"
        
        mock_service = AsyncMock()
        mock_service.get_delivery_information_list.return_value = {
            "success": True,
            "message": "Delivery list retrieved successfully",
            "data": {"deliveries": [], "total_count": 0}
        }
        
        with patch.object(agency_service, 'get_delivery_information_list', mock_service.get_delivery_information_list):
            # When
            response = client.post(
                f"/api/v1/agency/delivery/list/{delivery_date}",
                headers=auth_headers,
                params={"status": "pending", "page": 2, "size": 20}
            )
            
            # Then
            assert response.status_code == 200
            # 서비스 메서드가 올바른 파라미터로 호출되었는지 확인
            mock_service.get_delivery_information_list.assert_called_once()
            call_args = mock_service.get_delivery_information_list.call_args
            assert call_args[1]["status"] == "pending"
            assert call_args[1]["page"] == 2
            assert call_args[1]["size"] == 20
    
    def test_get_postal_code_info_success(self, client, auth_headers):
        """우편번호 정보 조회 성공 테스트"""
        # Given
        zipcode = "12345"
        
        mock_service = AsyncMock()
        mock_service.get_postal_code_information.return_value = {
            "success": True,
            "message": "Postal code info retrieved successfully",
            "data": {
                "zipcode": "12345",
                "sido": "서울시",
                "sigungu": "강남구",
                "is_deliverable": True
            }
        }
        
        with patch.object(agency_service, 'get_postal_code_information', mock_service.get_postal_code_information):
            # When
            response = client.get(
                f"/api/v1/agency/postalcode/{zipcode}",
                headers=auth_headers
            )
            
            # Then
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["zipcode"] == zipcode
    
    def test_service_error_handling(self, client):
        """서비스 에러 처리 테스트"""
        # Given
        mock_service = AsyncMock()
        mock_service.health_check.side_effect = Exception("Service error")
        
        with patch.object(agency_service, 'health_check', mock_service.health_check):
            # When
            response = client.get("/api/v1/agency/health")
            
            # Then
            assert response.status_code == 500
            data = response.json()
            assert "Service health check failed" in data["detail"]