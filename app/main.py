from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models import Service, CheckResult
from app.api import api_router
from app.services.scheduler import start_scheduler
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Monitor de Infraestrutura",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}