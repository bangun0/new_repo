"""
기본 스키마 클래스
API 요청/응답을 위한 Pydantic 모델들의 베이스 클래스를 정의합니다.
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel as PydanticBaseModel, Field


class BaseResponse(PydanticBaseModel):
    """
    기본 응답 스키마
    모든 API 응답의 베이스 스키마입니다.
    """
    success: bool = Field(..., description="요청 성공 여부")
    message: Optional[str] = Field(None, description="응답 메시지")
    data: Optional[Any] = Field(None, description="응답 데이터")
    error_code: Optional[str] = Field(None, description="에러 코드")


class BaseRequest(PydanticBaseModel):
    """
    기본 요청 스키마
    공통 요청 필드를 포함하는 베이스 스키마입니다.
    """
    model_config = {"from_attributes": True, "populate_by_name": True}


class AuthHeaders(PydanticBaseModel):
    """
    인증 헤더 스키마
    API 호출에 필요한 인증 정보를 담습니다.
    """
    authorization: str = Field(..., description="인증 토큰", alias="Authorization")
    agency_id: str = Field(..., description="대리점 ID", alias="AgencyId")
    
    model_config = {"populate_by_name": True}


class PaginationParams(PydanticBaseModel):
    """
    페이지네이션 파라미터 스키마
    """
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(10, ge=1, le=100, description="페이지 크기")
    
    
class PaginatedResponse(BaseResponse):
    """
    페이지네이션 응답 스키마
    """
    total_count: Optional[int] = Field(None, description="전체 항목 수")
    page: Optional[int] = Field(None, description="현재 페이지")
    size: Optional[int] = Field(None, description="페이지 크기")
    total_pages: Optional[int] = Field(None, description="전체 페이지 수")