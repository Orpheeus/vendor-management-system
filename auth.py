from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

# Configuracion del algoritmo de encriptacion (bcrypt es el estandar)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funcion 1: Recibe la contraseña plana y regresa el hash ilegible
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Funcion 2: Compara la contraseña que escribe el usuario con el hash de la DB
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# No compartir en GitHub
SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acess_token(data: dict):
    to_encode = data.copy()
    # Calculamos cuando va a caducar el token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Creamos el token firmado con nuestra SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt