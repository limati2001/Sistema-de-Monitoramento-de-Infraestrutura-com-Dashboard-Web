from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.service import Service
from app.models.check_result import CheckResult
from app.services.monitor import check_service
from typing import List

router = APIRouter(prefix="/monitor", tags=["monitor"])

@router.get("/{service_id}")
async def check_now(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    result = await check_service(service.protocol, service.host, service.port)
    
    db_result = CheckResult(
        service_id=service_id,
        status=result["status"],
        status_code=result.get("status_code"),
        latency_ms=result.get("latency_ms"),
        error=result.get("error")
    )
    db.add(db_result)
    db.commit()

    return {"service": service.name, **result}

@router.get("/{service_id}/history")
def get_history(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    results = (
        db.query(CheckResult)
        .filter(CheckResult.service_id == service_id)
        .order_by(CheckResult.checked_at.desc())
        .limit(50)
        .all()
    )
    return {"service": service.name, "history": results}