from fastapi import APIRouter
from app.api.services import router as services_router
from app.api.monitor import router as monitor_router
from app.api.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(services_router)
api_router.include_router(monitor_router)
api_router.include_router(dashboard_router)