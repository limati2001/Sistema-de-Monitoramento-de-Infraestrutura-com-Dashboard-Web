from pydantic import BaseModel
from typing import Optional

class ServiceCreate(BaseModel):
    name: str
    host: str
    port: Optional[int] = None
    protocol: str = "http"

class ServiceResponse(BaseModel):
    id: int
    name: str
    host: str
    port: Optional[int]
    protocol: str
    is_active: bool

    class Config:
        from_attributes = True