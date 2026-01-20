from pydantic import BaseModel
from datetime import datetime
from app.modelos.database import StatusEvento

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    role: str

    model_config = {"from_attributes": True}

class EventoResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    data_inicio: datetime
    data_fim: datetime
    local: str
    link: str
    status: StatusEvento

    origem: str
    status: str
    classificacao: str

    usuario_id: int
    categoria_id: int

    model_config = {"from_attributes": True}

class CategoriaResponse(BaseModel):
    id: int
    categoria: str

    model_config = {"from_attributes": True}