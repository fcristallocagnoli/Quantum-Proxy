import ast
import time
from datetime import datetime
from pathlib import Path

import wikipediaapi
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


def norm_id(db_document: dict) -> str:
    """Extracts the id from a MongoDB document and returns it as a string."""
    return str(db_document["_id"])


def norm_str(value: str) -> str:
    """Normalize a string value."""
    return value.lower().replace(" ", "_")


def is_first_account():
    # must be == 0
    return count_documents("users") == 1


# region Date related


def convert_from_ms(millisec: int) -> str:
    """
    Convierte tiempo en milisegundos a tiempo de espera con el formato de IonQ
    """
    # Convertir milisegundos a segundos
    seconds = millisec // 1000

    # Calcular días, horas y minutos
    mins, seconds = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)

    avg_time_in_queue = ""

    if days > 30:
        avg_time_in_queue = "> 1month"
    elif days > 1:
        avg_time_in_queue = f"{days}d {hours}hrs {mins}min"
    elif hours > 1:
        avg_time_in_queue = f"{hours}hrs {mins}min"
    elif mins > 1:
        avg_time_in_queue = f"{mins}min"
    else:
        avg_time_in_queue = "< 1min"

    return avg_time_in_queue


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


def get_wiki_content(wiki_name: str):
    """
    Extrae el contenido de la página de Wikipedia.
    - Para rellenar la descripción de los proveedores
    """
    wiki_html = wikipediaapi.Wikipedia(
        user_agent="Quantum-Proxy (tfg.quantum.proxy@gmail.com)",
        language="en",
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )
    if not (page := wiki_html.page(wiki_name)).exists():
        # logger.debug(f"Page {wiki_name} does not exist")
        return ""

    return f"<h2>Summary:</h2>{page.summary}<h2>History:</h2>{page.section_by_title('History').text}"
