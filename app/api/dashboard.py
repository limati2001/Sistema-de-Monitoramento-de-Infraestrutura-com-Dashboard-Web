from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.service import Service
from app.models.check_result import CheckResult

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard(db: Session = Depends(get_db)):
    services = db.query(Service).filter(Service.is_active == True).all()
    
    cards = ""
    for service in services:
        last = (
            db.query(CheckResult)
            .filter(CheckResult.service_id == service.id)
            .order_by(CheckResult.checked_at.desc())
            .first()
        )
        
        if last:
            status = last.status
            latency = f"{last.latency_ms:.1f}ms" if last.latency_ms else "—"
            checked = last.checked_at.strftime("%H:%M:%S")
        else:
            status = "unknown"
            latency = "—"
            checked = "Nunca checado"
        
        color = "#22c55e" if status == "up" else "#ef4444" if status == "down" else "#94a3b8"
        label = "UP" if status == "up" else "DOWN" if status == "down" else "?"
        
        cards += f"""
        <div class="card">
            <div class="status-dot" style="background:{color}"></div>
            <div class="info">
                <h2>{service.name}</h2>
                <p>{service.host}:{service.port}</p>
            </div>
            <div class="metrics">
                <span class="badge" style="background:{color}">{label}</span>
                <span class="latency">{latency}</span>
                <span class="time">Último check: {checked}</span>
            </div>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="30">
        <title>Monitor de Infraestrutura</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                min-height: 100vh;
                padding: 2rem;
            }}
            header {{
                margin-bottom: 2rem;
            }}
            header h1 {{
                font-size: 1.8rem;
                font-weight: 700;
                color: #f8fafc;
            }}
            header p {{
                color: #64748b;
                margin-top: 0.25rem;
                font-size: 0.9rem;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
                gap: 1rem;
            }}
            .card {{
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 1.5rem;
                display: flex;
                align-items: center;
                gap: 1rem;
            }}
            .status-dot {{
                width: 12px;
                height: 12px;
                border-radius: 50%;
                flex-shrink: 0;
            }}
            .info {{ flex: 1; }}
            .info h2 {{ font-size: 1rem; font-weight: 600; }}
            .info p {{ font-size: 0.8rem; color: #64748b; margin-top: 0.2rem; }}
            .metrics {{
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 0.3rem;
            }}
            .badge {{
                font-size: 0.75rem;
                font-weight: 700;
                padding: 0.2rem 0.6rem;
                border-radius: 999px;
                color: white;
            }}
            .latency {{ font-size: 0.9rem; font-weight: 600; color: #94a3b8; }}
            .time {{ font-size: 0.7rem; color: #475569; }}
        </style>
    </head>
    <body>
        <header>
            <h1>🖥️ Monitor de Infraestrutura</h1>
            <p>Atualiza automaticamente a cada 30 segundos</p>
        </header>
        <div class="grid">
            {cards}
        </div>
    </body>
    </html>
    """
    return html