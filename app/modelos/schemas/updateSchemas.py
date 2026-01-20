from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None

    class Config:
        from_attributes = True

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    local: Optional[str] = None
    categoria_id: Optional[int] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None

    class Config:
        from_attributes = True