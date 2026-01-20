import enum
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship

# criar conexão com o banco de dados SQLite
engine = create_engine("sqlite:///eventos.db")
Base = declarative_base()

# definição das tabelas do banco de dados

class Role(enum.Enum):
    admin = "admin"
    user = "user"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    ativo = Column(Boolean, default=True)

    eventos = relationship("Evento", back_populates="usuario")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    categoria = Column(String, nullable=False, unique=True)

    eventos = relationship("Evento", back_populates="categoria")

class StatusEvento(enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

class OrigemEvento(enum.Enum):
    OFICIAL = "OFICIAL"
    NAO_OFICIAL = "NÃO OFICIAL"

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    local = Column(String, nullable=False)
    link = Column(String, nullable=True) # nem todo evento tem link

    origem = Column(String, default="NÃO OFICIAL", nullable=False)
    status = Column(Enum(StatusEvento), default=StatusEvento.PENDENTE, nullable=False)
    classificacao = Column(String, default="Público", nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="eventos")
    categoria = relationship("Categoria", back_populates="eventos")

# criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
