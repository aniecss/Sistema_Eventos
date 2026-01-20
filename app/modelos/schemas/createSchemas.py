from pydantic import BaseModel
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str


class LoginCreate(BaseModel):
    email: str
    senha: str


class EventoCreate(BaseModel):
    titulo: str
    descricao: str
    data_inicio: datetime
    data_fim: datetime
    local: str
    categoria_id: int
    link: str | None = None

class CategoriaCreate(BaseModel):
    categoria: str

class UsuarioCreateAdmin(BaseModel):
    nome: str
    email: str
    senha: str
    role: str
