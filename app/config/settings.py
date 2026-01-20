import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITMO = os.getenv("ALGORITMO", "HS256")
TOKEN_EXPIRA = int(os.getenv("TOKEN_EXPIRA", 30))

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não carregada")
