from fastapi import APIRouter
from app.api.services import router as services_router

api_router = APIRouter()
api_router.include_router(services_router)