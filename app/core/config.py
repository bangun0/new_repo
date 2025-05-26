"""
애플리케이션 설정 관리
환경변수 및 기본 설정값들을 관리합니다.
"""
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    환경변수를 통해 설정값을 로드합니다.
    """
    
    # API 기본 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TodayPickup API Client"
    
    # TodayPickup API 설정
    TODAYPICKUP_BASE_URL: str = "https://admin.todaypickup.com"
    TODAYPICKUP_API_PREFIX: str = "/api"
    
    # 인증 설정
    DEFAULT_AGENCY_ID: str = ""
    DEFAULT_AUTH_TOKEN: str = ""
    
    # CORS 설정
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # HTTP 클라이언트 설정
    HTTP_TIMEOUT: int = 30
    HTTP_RETRIES: int = 3
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic 설정"""
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()