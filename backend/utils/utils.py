from datetime import datetime
from passlib.context import CryptContext

# region Miscelaneous


def norm_id(db_document: dict) -> str:
    """Extracts the id from a MongoDB document and returns it as a string."""
    return str(db_document["_id"])


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


def get_current_time() -> str:
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
    return date.strftime("%Y-%m-%d %H:%M:%S GMT%z")


# region Password hashing

pwd_context = CryptContext(schemes=["bcrypt", "unix_disabled"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)
