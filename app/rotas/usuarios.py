from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.modelos.database import Usuario
from app.modelos.schemas.createSchemas import UsuarioCreate, LoginCreate
from app.modelos.schemas.responseSchemas import UsuarioResponse
from app.modelos.schemas.updateSchemas import UsuarioUpdate
from app.config.permissoes.permissoes import admin_required
from app.config.database import get_db
from app.config.autenticacao import (criar_token, oauth2_scheme, validar_refresh_token, get_usuario)
from app.config.security import hash_senha, verificar_senha
from app.config.settings import TOKEN_EXPIRA


usuarios_router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@usuarios_router.get("/me", response_model=UsuarioResponse)
async def usuario_logado(usuario: Usuario = Depends(get_usuario)):
    return usuario

@usuarios_router.post("/criar_usuario")
async def criar_usuario(usuario: UsuarioCreate, session: Session = Depends(get_db)):
    usuario_existente = session.query(Usuario).filter(Usuario.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    senha_criptografada = hash_senha(usuario.senha)
    
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_criptografada,
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return {"msg": "Usuário criado com sucesso", "usuario_id": novo_usuario.id}

@usuarios_router.post("/login")
async def login(login: LoginCreate, session: Session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email == login.email).first()

    if not usuario or not usuario.ativo or not verificar_senha(login.senha, usuario.senha):
        raise HTTPException(status_code=401, detail="Login inválido")

    access_token = criar_token(
        {"sub": str(usuario.id), "type": "access"},
        duracao=timedelta(minutes=TOKEN_EXPIRA)
    )

    refresh_token = criar_token(
        {"sub": str(usuario.id), "type": "refresh"},
        duracao=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@usuarios_router.post("/formulario_login")
async def login_formulario(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    # preencher o formulário
    usuario = session.query(Usuario).filter(Usuario.email == dados_formulario.username).first()

    if not usuario or not usuario.ativo:
        raise HTTPException(status_code=401, detail="Usuário inválido")
    
    if not verificar_senha(dados_formulario.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Senha inválida")
    
    token = criar_token(
    {"sub": str(usuario.id), "type": "access"},
    duracao=timedelta(minutes=TOKEN_EXPIRA)
)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@usuarios_router.post("/refresh")
async def refresh_token(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    usuario_id = validar_refresh_token(token)

    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    novo_access = criar_token(
        {"sub": str(usuario.id), "type": "access"},
        duracao=timedelta(minutes=TOKEN_EXPIRA)
    )

    return {
        "access_token": novo_access,
        "token_type": "bearer"
    }

@usuarios_router.put("/me")
async def editar_perfil(novos_dados: UsuarioUpdate, session: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario)):

    if novos_dados.nome:
        usuario.nome = novos_dados.nome

    if novos_dados.senha:
        usuario.senha = hash_senha(novos_dados.senha)

    session.commit()
    session.refresh(usuario)

    return {"Mensagem": "Perfil atualizado com sucesso"}

@usuarios_router.delete("/me")
async def deletar_conta(session: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario)):
    usuario.ativo = False
    session.commit()

    return {"Mensagem": "Conta desativada com sucesso"}

@usuarios_router.delete("/{id}")
async def admin_deleta(id: int, session: Session = Depends(get_db), usuario_logado: Usuario = Depends(admin_required)):
    usuario = session.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if usuario_logado.id == id:
        raise HTTPException(status_code=400, detail="Use /usuarios/me")

    usuario.ativo = False
    session.commit()

    return {"msg": "Usuário desativado"}
