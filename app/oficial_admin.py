from app.config.database import SessionLocal
from app.modelos.database import Usuario
from app.config.security import hash_senha

db = SessionLocal()

email = "oficial@teste.com"

admin_existe = db.query(Usuario).filter(Usuario.email == email).first()

if admin_existe:
    print("Perfil oficial já existe")
else:
    admin = Usuario(
        nome="Perfil Oficial",
        email=email,
        senha=hash_senha("admin123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    print("Perfil oficial criado com sucesso")

db.close()