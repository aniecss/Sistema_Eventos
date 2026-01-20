from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modelos.database import Evento, Usuario, StatusEvento
from app.modelos.schemas.createSchemas import EventoCreate
from app.modelos.schemas.responseSchemas import EventoResponse
from app.modelos.schemas.updateSchemas import EventoUpdate
from app.config.database import get_db
from app.config.autenticacao import get_usuario

eventos_router = APIRouter(prefix="/eventos", tags=["Eventos"])

@eventos_router.post("/", response_model=EventoResponse)
def criar_evento(evento: EventoCreate, usuario_logado: Usuario = Depends(get_usuario), session: Session = Depends(get_db)):
    novo_evento = Evento(
        titulo=evento.titulo,
        descricao=evento.descricao,
        data_inicio=evento.data_inicio,
        data_fim=evento.data_fim,
        local=evento.local,
        categoria_id=evento.categoria_id,
        usuario_id=usuario_logado.id,
        link=evento.link,
        status="PENDENTE"
    )

    session.add(novo_evento)
    session.commit()
    session.refresh(novo_evento)

    return novo_evento

@eventos_router.get("/", response_model=list[EventoResponse])
async def buscar_eventos(session: Session = Depends(get_db)):
    eventos = (session.query(Evento).filter(Evento.status == "APROVADO").all())
    return eventos

@eventos_router.get("/meus")
async def listar_eventos_usuario(usuario: Usuario = Depends(get_usuario), session: Session = Depends(get_db)):
    eventos = session.query(Evento).filter(Evento.usuario_id == usuario.id).all()

    if not eventos:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado para este usuário")

    return eventos

@eventos_router.get("/filtrar", response_model=list[EventoResponse])
async def filtrar_eventos(
    session: Session = Depends(get_db),
    categoria_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    titulo: Optional[str] = None
):
    query = session.query(Evento).filter(Evento.status == StatusEvento.APROVADO)

    if categoria_id:
        query = query.filter(Evento.categoria_id == categoria_id)

    if data_inicio:
        query = query.filter(Evento.data_inicio >= data_inicio)

    if data_fim:
        query = query.filter(Evento.data_fim <= data_fim)

    if titulo:
        query = query.filter(Evento.titulo.ilike(f"%{titulo}%"))

    return query.all()

@eventos_router.get("/{id}", response_model=EventoResponse)
async def obter_evento(id: int, session: Session = Depends(get_db)):
    evento = session.query(Evento).filter(
        Evento.id == id,
        Evento.status == StatusEvento.APROVADO
    ).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    return evento

@eventos_router.put("/{id}", response_model=EventoResponse)
async def editar_evento(id: int, dados: EventoUpdate, session: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario)):
    evento = session.query(Evento).filter(Evento.id == id).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if usuario.role != "admin" and evento.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(evento, campo, valor)

    session.commit()
    session.refresh(evento)

    return evento


@eventos_router.delete("/{id}")
async def cancelar_evento(id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario)):
    evento = session.query(Evento).filter(Evento.id == id).first()

    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if usuario.role != "admin" and evento.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar esse evento")

    evento.status = StatusEvento.CANCELADO
    session.commit()

    return {"msg": "Evento cancelado"}


@eventos_router.get("/criar/eventos/oficial")
def criar_evento_oficial(dados: EventoCreate, session: Session = Depends(get_db)):
    novo = Evento(
        titulo=dados.titulo,
        descricao=dados.descricao,
        data_inicio=dados.data_inicio,
        data_fim=dados.data_fim,
        local=dados.local,
        link=dados.link,
        status=StatusEvento.APROVADO,
        origem="OFICIAL"
    )

    session.add(novo)
    session.commit()
    session.refresh(novo)

    return novo