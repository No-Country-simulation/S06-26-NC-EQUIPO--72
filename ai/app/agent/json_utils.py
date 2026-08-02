from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any


def json_default(obj: Any) -> Any:
    """
    Convierte tipos que json.dumps no soporta nativamente pero que
    MySQL/aiomysql devuelven con frecuencia: TIME -> timedelta,
    DATE/DATETIME -> date/datetime, DECIMAL -> Decimal.
    """
    if isinstance(obj, timedelta):
        # timedelta representa TIME en MySQL - lo pasamos a "HH:MM:SS"
        total_seconds = int(obj.total_seconds())
        horas, resto = divmod(total_seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
