from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import Service
from app.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Monitor de Infraestrutura", version="0.1.0")

app.include_router(api_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}