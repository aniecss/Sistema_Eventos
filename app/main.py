from fastapi import FastAPI
from app.rotas.usuarios import usuarios_router
from app.rotas.eventos import eventos_router
from app.rotas.categoria import categoria_router
from app.rotas.admin import admin_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sistema de Eventos", description="API para gerenciamento de eventos", version="1.0.0")

app.include_router(usuarios_router)
app.include_router(eventos_router)
app.include_router(categoria_router)
app.include_router(admin_router)

# uvicorn app.main:app --reload 
