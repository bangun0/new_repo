"""Entry point for the FastAPI application."""
from fastapi import FastAPI
from .controllers import agency, mall

app = FastAPI(title="TodayPickup API Proxy")

app.include_router(agency.router)
app.include_router(mall.router)

