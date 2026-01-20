from sqlalchemy.orm import sessionmaker
from app.modelos.database import engine

"""
Este código tem como objetivo centralizar as depedências para não ter que iniciar e fechar as sessões todas as rotas, apenas ser chamada
Session → executa o banco de dados
sessionmaker →  criar uma sessões configuradas
"""

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()