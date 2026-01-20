from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config.settings import SECRET_KEY, ALGORITMO

from app.modelos.database import Usuario
from app.config.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/formulario_login")

def criar_token(dados: dict, duracao: timedelta = timedelta(minutes=30)) -> str:
    to_encode = dados.copy()
    expira = datetime.utcnow() + duracao

    to_encode.update({"exp": expira})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITMO)


def get_usuario(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credencial_invalida = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])

        if payload.get("type") != "access":
            raise credencial_invalida

        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise credencial_invalida

    except JWTError:
        raise credencial_invalida

    usuario = db.query(Usuario).filter(
        Usuario.id == int(usuario_id),
        Usuario.ativo == True
    ).first()

    if not usuario:
        raise credencial_invalida

    return usuario

def validar_refresh_token(token: str):
    token_invalido = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido ou expirado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])

        if payload.get("type") != "refresh":
            raise token_invalido

        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise token_invalido

        return int(usuario_id)

    except (JWTError, ValueError, TypeError):
        raise token_invalido
