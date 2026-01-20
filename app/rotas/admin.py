from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.modelos.database import Usuario, Evento, StatusEvento
from app.config.database import get_db
from app.config.permissoes.permissoes import admin_required

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

# eventos pendentes
@admin_router.get("/eventos/pendentes")
async def listar_eventos_pendentes(session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    eventos = session.query(Evento).filter(Evento.status == StatusEvento.PENDENTE).all()

    return eventos

# aprovar evento
@admin_router.put("/eventos/{id}/aprovar")
async def aprovar_evento(id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    evento = session.query(Evento).filter(Evento.id == id).first()

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    
    evento.status = "APROVADO"
    session.commit()
    session.refresh(evento)

    return {"Mensagem": "Evento aprovado com sucesso.", 
            "evento": evento}

# rejeitar evento
@admin_router.put("/eventos/{id}/rejeitar")
async def rejeitar_evento(id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    evento = session.query(Evento).filter(Evento.id == id).first()

    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado.")
    
    evento.status = "REJEITADO"
    session.commit()
    session.refresh(evento)

    return {"Mensagem": "Evento rejeitado com sucesso.", 
            "evento": evento}

# listar todos os usuarios
@admin_router.get("/usuarios")
async def listar_usuarios(session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    usuarios = session.query(Usuario).all()

    return usuarios

# deletar usuario
@admin_router.delete("/usuarios/{id}")
async def deletar_usuario(id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    usuario_a_deletar = session.query(Usuario).filter(Usuario.id == id).first()

    if not usuario_a_deletar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    session.delete(usuario_a_deletar)
    session.commit()

    return {"Mensagem": "Usuário deletado com sucesso."}