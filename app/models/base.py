"""
기본 모델 클래스
모든 모델의 베이스 클래스를 정의합니다.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class BaseModel:
    """
    기본 모델 클래스
    모든 모델이 상속받는 베이스 클래스입니다.
    """
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AuthInfo:
    """
    인증 정보 모델
    API 호출에 필요한 인증 정보를 담습니다.
    """
    agency_id: str
    auth_token: str
    
    def to_headers(self) -> dict:
        """
        인증 정보를 HTTP 헤더 형태로 변환합니다.
        
        Returns:
            dict: 인증 헤더 딕셔너리
        """
        return {
            "Authorization": self.auth_token,
            "AgencyId": self.agency_id
        }