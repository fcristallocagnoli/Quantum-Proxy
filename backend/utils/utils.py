import ast
import time
from datetime import datetime
from pathlib import Path

from bson import ObjectId
from database.mongo_client import count_documents
from fastapi import HTTPException, status
from passlib.context import CryptContext

# region Miscelaneous


def sf_parse_object_id(id: str | int) -> ObjectId:
    """
    Safe parse from str to ObjectId.
    :raises HTTPException 400: if the id is not valid
    """
    id = str(id) if isinstance(id, int) else id
    try:
        object_id = ObjectId(id)
        return object_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id {e}"
        )


def create_bid(backend: dict):
    """
    Create a unique backend id
    """
    backend_name: str = backend["backend_name"]
    backend_name = backend_name.lower().replace(" ", "-")
 
    provider: dict = backend["provider"]
    provider_from: str = provider.get("provider_from")

    if provider_from:
        provider_from = provider_from.lower()
        return f"{backend_name}-{provider_from}"

    return backend_name


def norm_id(db_document: dict) -> str:
    """Extracts the id from a MongoDB document and returns it as a string."""
    return str(db_document["_id"])


def norm_str(value: str) -> str:
    """Normalize a string value."""
    return value.lower().replace(" ", "_")


# sera 1 si esta la dummy account, sera 0 si no lo esta
# (en principio no estará, se mete luego)
def is_first_account():
    # must be == 0
    return count_documents("users") == 0


# region Date related


def from_seconds_to_date(seconds) -> str:
    """Convierte y formatea a fecha a partir de tiempo en segundos"""
    date: datetime = datetime.fromtimestamp(seconds)
    return format_date(date)


def get_timestamp():
    return time.time()


def get_current_datetime() -> datetime:
    return datetime.now()


def get_current_time_iso() -> str:
    """
    Devuelve la fecha actual con formato ISO-8601
    """
    return format_date(datetime.now())


def fromisoformat(date: str) -> str:
    """
    Convierte un string con formato ISO-8601 a un objeto datetime
    """
    return format_date(datetime.fromisoformat(date))


def format_date(date: datetime) -> str:
    """
    Formatea una fecha a un string con el formato ISO-8601
    """
    # return date.strftime("%Y-%m-%d %H:%M:%S GMT%z")
    return date.isoformat()


# region Password hashing

pwd_context = CryptContext(schemes=["bcrypt", "unix_disabled"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


# region Code validation


def parse_code(code: str):
    """
    Validar el código antes de ejecutarlo.
    - Evitar llamadas a funciones peligrosas como eval() o exec().
    """
    arbol = ast.parse(code)

    # Recorrer el árbol y realizar operaciones de validación
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            # Verificar si hay llamadas a funciones peligrosas
            if nodo.func.id in ["eval", "exec"]:
                raise ValueError(
                    "El código no puede contener llamadas a funciones peligrosas como eval() o exec()"
                )


def check_code(file_path: Path):
    """
    Parse and check the code before executing it.
    - Avoid calls to dangerous functions like eval() or exec().
    """
    if not file_path.exists():
        print(f"File {file_path.name} not found.")
        return False
    with open(file_path, encoding="utf-8") as f:
        code = f.read()
    try:
        parse_code(code)
    except Exception as e:
        match error := type(e).__name__:
            case ValueError.__name__:
                print(f"{error}: Error de sintaxis en el código\n", e)
            case SyntaxError.__name__:
                print(f"{error}: Error al validar el código\n", e)
            case _:
                print(f"{error}: Error al ejecutar el código\n", e)
                # raise type("ParseException", (Exception,), {"msg": error})
        return False
    return True
