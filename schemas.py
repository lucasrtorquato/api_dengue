from pydantic import BaseModel
from typing import Optional

class FocoCreate(BaseModel):
    tipo: str

    rua: str
    numero: str
    bairro: str
    complemento: Optional[str] = None
    cidade: str
    estado: str
    cep: str
    latitude: float
    longitude: float


class FocoResponse(FocoCreate):
    id: int
    status: str

    class Config:
        from_attributes = True