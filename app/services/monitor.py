import httpx
import socket
import asyncio
from datetime import datetime

async def check_http(host: str, port: int = 443) -> dict:
    url = f"https://{host}" if port == 443 else f"http://{host}:{port}"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            start = asyncio.get_event_loop().time()
            response = await client.get(url)
            latency = (asyncio.get_event_loop().time() - start) * 1000
            return {
                "status": "up",
                "status_code": response.status_code,
                "latency_ms": round(latency, 2),
                "checked_at": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "down",
            "error": str(e),
            "latency_ms": None,
            "checked_at": datetime.utcnow().isoformat()
        }

async def check_tcp(host: str, port: int) -> dict:
    try:
        start = asyncio.get_event_loop().time()
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=5.0
        )
        latency = (asyncio.get_event_loop().time() - start) * 1000
        writer.close()
        return {
            "status": "up",
            "latency_ms": round(latency, 2),
            "checked_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "down",
            "error": str(e),
            "latency_ms": None,
            "checked_at": datetime.utcnow().isoformat()
        }

async def check_service(protocol: str, host: str, port: int = None) -> dict:
    if protocol == "http":
        return await check_http(host, port or 80)
    elif protocol == "tcp":
        return await check_tcp(host, port or 80)
    else:
        return {"status": "unknown", "error": "Protocolo não suportado"}