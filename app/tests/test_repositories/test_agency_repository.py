"""
AgencyRepository 단위 테스트
대리점 Repository의 기능을 테스트합니다.
"""
import pytest
from unittest.mock import AsyncMock, patch
import httpx

from app.repositories.agency_repository import AgencyRepository
from app.models.base import AuthInfo
from app.schemas.agency import TokenGenerationRequest, TokenValidationRequest, DeliveryAssignmentRequest


class TestAgencyRepository:
    """AgencyRepository 테스트 클래스"""
    
    @pytest.fixture
    def repository(self):
        """AgencyRepository 인스턴스 생성"""
        return AgencyRepository()
    
    @pytest.mark.asyncio
    async def test_health_check_success(self, repository, mock_http_client):
        """헬스체크 성공 테스트"""
        # Given
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.health_check()
            
            # Then
            assert result is True
            mock_http_client.get.assert_called_once_with("/")
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self, repository):
        """헬스체크 실패 테스트"""
        # Given
        mock_client = AsyncMock()
        mock_client.get.side_effect = httpx.HTTPError("Connection failed")
        
        with patch.object(repository, 'http_client', mock_client):
            # When
            result = await repository.health_check()
            
            # Then
            assert result is False
    
    @pytest.mark.asyncio
    async def test_generate_token_success(self, repository, mock_http_client, mock_http_response):
        """토큰 생성 성공 테스트"""
        # Given
        request = TokenGenerationRequest(agency_id="test_agency", api_key="test_key")
        expected_response = {
            "access_token": "test_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        mock_response = mock_http_response(200, expected_response)
        mock_http_client.post.return_value = mock_response
        
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.generate_token(request)
            
            # Then
            assert result == expected_response
            mock_http_client.post.assert_called_once_with(
                endpoint="/api/agency/auth/token",
                json_data=request.dict()
            )
    
    @pytest.mark.asyncio
    async def test_validate_token_success(self, repository, mock_http_client, mock_http_response, mock_auth_info):
        """토큰 검증 성공 테스트"""
        # Given
        request = TokenValidationRequest(token="test_token")
        expected_response = {
            "is_valid": True,
            "expires_at": "2024-12-31T23:59:59",
            "agency_id": "test_agency"
        }
        
        mock_response = mock_http_response(200, expected_response)
        mock_http_client.post.return_value = mock_response
        
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.validate_token(request, mock_auth_info)
            
            # Then
            assert result == expected_response
            mock_http_client.post.assert_called_once_with(
                endpoint="/api/agency/auth",
                headers=mock_auth_info.to_headers(),
                json_data=request.dict()
            )
    
    @pytest.mark.asyncio
    async def test_assign_delivery_success(self, repository, mock_http_client, mock_http_response, mock_auth_info):
        """배송 배정 성공 테스트"""
        # Given
        request = DeliveryAssignmentRequest(
            invoice_number="INV123456",
            driver_name="홍길동",
            driver_phone="010-1234-5678"
        )
        expected_response = {
            "invoice_number": "INV123456",
            "assigned_at": "2024-01-01T00:00:00"
        }
        
        mock_response = mock_http_response(200, expected_response)
        mock_http_client.put.return_value = mock_response
        
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.assign_delivery(request, mock_auth_info)
            
            # Then
            assert result == expected_response
            mock_http_client.put.assert_called_once_with(
                endpoint="/api/agency/delivery",
                headers=mock_auth_info.to_headers(),
                json_data=request.dict()
            )
    
    @pytest.mark.asyncio
    async def test_get_delivery_list_success(self, repository, mock_http_client, mock_http_response, mock_auth_info):
        """배송 목록 조회 성공 테스트"""
        # Given
        delivery_date = "2024-01-01"
        expected_response = {
            "deliveries": [],
            "total_count": 0,
            "page": 1,
            "total_pages": 0
        }
        
        mock_response = mock_http_response(200, expected_response)
        mock_http_client.post.return_value = mock_response
        
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.get_delivery_list(
                delivery_date=delivery_date,
                auth_info=mock_auth_info,
                status="pending",
                page=1,
                size=10
            )
            
            # Then
            assert result == expected_response
            mock_http_client.post.assert_called_once_with(
                endpoint=f"/api/agency/delivery/list/{delivery_date}",
                headers=mock_auth_info.to_headers(),
                params={"status": "pending", "page": 1, "size": 10}
            )
    
    @pytest.mark.asyncio
    async def test_get_postal_code_info_success(self, repository, mock_http_client, mock_http_response, mock_auth_info):
        """우편번호 정보 조회 성공 테스트"""
        # Given
        zipcode = "12345"
        expected_response = {
            "zipcode": "12345",
            "sido": "서울시",
            "sigungu": "강남구",
            "dong": "역삼동",
            "is_deliverable": True,
            "delivery_fee": 3000
        }
        
        mock_response = mock_http_response(200, expected_response)
        mock_http_client.get.return_value = mock_response
        
        with patch.object(repository, 'http_client', mock_http_client):
            # When
            result = await repository.get_postal_code_info(zipcode, mock_auth_info)
            
            # Then
            assert result == expected_response
            mock_http_client.get.assert_called_once_with(
                endpoint=f"/api/agency/postalcode/{zipcode}",
                headers=mock_auth_info.to_headers()
            )
    
    @pytest.mark.asyncio
    async def test_handle_response_error(self, repository):
        """응답 처리 에러 테스트"""
        # Given
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Bad Request", request=mock_response, response=mock_response
        )
        mock_response.json.return_value = {"error": "Invalid request"}
        
        # When & Then
        with pytest.raises(Exception) as exc_info:
            await repository._handle_response(mock_response)
        
        assert "API Error" in str(exc_info.value)