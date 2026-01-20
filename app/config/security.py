from passlib.context import CryptContext

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_senha(senha: str) -> str:
    return bcrypt_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return bcrypt_context.verify(senha_plana, senha_hash)