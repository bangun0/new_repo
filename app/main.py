"""
FastAPI 애플리케이션 메인 엔트리포인트
TodayPickup API 클라이언트 서비스를 제공합니다.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.agency_controller import router as agency_router
from app.controllers.mall_controller import router as mall_router
from app.core.config import settings

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="TodayPickup API Client",
    description="TodayPickup Admin API를 호출하기 위한 FastAPI 클라이언트",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(agency_router, prefix="/api/v1/agency", tags=["Agency"])
app.include_router(mall_router, prefix="/api/v1/mall", tags=["Mall"])


@app.get("/")
async def root():
    """
    루트 엔드포인트 - API 상태 확인
    
    Returns:
        dict: API 상태 정보
    """
    return {
        "message": "TodayPickup API Client",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """
    헬스 체크 엔드포인트
    
    Returns:
        dict: 서비스 상태 정보
    """
    return {"status": "healthy", "service": "todaypickup-api-client"}