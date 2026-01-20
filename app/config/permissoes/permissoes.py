from fastapi import Depends, HTTPException
from app.config.autenticacao import get_usuario
from app.modelos.database import Usuario, Role

def admin_required(usuario: Usuario = Depends(get_usuario)):

    if usuario.role != Role.admin:
        raise HTTPException(
            status_code=403,
            detail="Acesso restrito a administradores"
        )
    return usuario