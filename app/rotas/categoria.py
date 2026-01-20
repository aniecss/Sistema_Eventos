from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.modelos.database import Categoria, Usuario
from app.modelos.schemas.createSchemas import CategoriaCreate
from app.modelos.schemas.updateSchemas import CategoriaUpdate
from app.config.database import get_db
from app.config.permissoes.permissoes import admin_required

categoria_router = APIRouter(prefix="/categorias", tags=["Categorias"])

@categoria_router.get("/")
async def listar_categorias(session: Session = Depends(get_db)):
    categorias = session.query(Categoria).all()

    return categorias

@categoria_router.post("/")
async def criar_categoria(dados: CategoriaCreate, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    categoria_existe = session.query(Categoria).filter(Categoria.categoria == dados.categoria).first()

    if categoria_existe:
        raise HTTPException(status_code=400, detail="Categoria já existe.")
    
    categoria = Categoria(categoria=dados.categoria)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria

@categoria_router.put("/{id}")
async def editar_categoria(id: int, dados: CategoriaUpdate, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    categoria = session.query(Categoria).filter(Categoria.id == id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    
    if dados.categoria:
        categoria.categoria = dados.categoria

    session.commit()
    session.refresh(categoria)

    return categoria

@categoria_router.delete("/{id}")
async def deletar_categoria(id: int, session: Session = Depends(get_db), usuario: Usuario = Depends(admin_required)):
    categoria = session.query(Categoria).filter(Categoria.id == id).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    
    session.delete(categoria)
    session.commit()

    return {"detail": "Categoria deletada com sucesso."}