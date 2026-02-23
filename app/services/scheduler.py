from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.service import Service
from app.models.check_result import CheckResult
from app.services.monitor import check_service
import logging

logger = logging.getLogger(__name__)

async def check_all_services():
    db: Session = SessionLocal()
    try:
        services = db.query(Service).filter(Service.is_active == True).all()
        logger.info(f"Checando {len(services)} serviços...")
        
        for service in services:
            result = await check_service(service.protocol, service.host, service.port)
            
            db_result = CheckResult(
                service_id=service.id,
                status=result["status"],
                status_code=result.get("status_code"),
                latency_ms=result.get("latency_ms"),
                error=result.get("error")
            )
            db.add(db_result)
            logger.info(f"{service.name} ({service.host}): {result['status']}")
        
        db.commit()
    except Exception as e:
        logger.error(f"Erro no scheduler: {e}")
    finally:
        db.close()

def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_all_services,
        trigger="interval",
        minutes=1,  # muda para o intervalo que quiser
        id="check_services",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler iniciado.")
    return scheduler