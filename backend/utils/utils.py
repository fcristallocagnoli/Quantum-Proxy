from datetime import datetime


def norm_id(db_document: dict) -> str:
    """Extracts the id from a MongoDB document and returns it as a string."""
    return str(db_document["_id"])


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
    return date.strftime("%Y-%m-%d %H:%M:%S GMT%z")


def get_current_time() -> str:
    """
    Devuelve la fecha actual con formato ISO-8601
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S GMT%z")
