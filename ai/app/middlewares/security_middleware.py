import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings


# Métodos/endpoints que exponen el agente (costosos en tokens).
_RUTAS_AGENTE = {("/consulta", "POST"), ("/consulta/respuesta", "POST")}


class SecurityMiddleware(BaseHTTPMiddleware):
    """ auth por API key (opt-in) + rate limit por IP.

    - Auth: si settings.api_auth_token está fijado, POST /consulta y
      /consulta/respuesta requieren el header X-API-Key con el valor exacto
      (comparación en tiempo constante). Si no está fijado, no se exige nada
      (compatibilidad con el backend actual).
    - Rate limit: ventana deslizante en memoria por IP de cliente. Solo aplica
      a las rutas del agente. Devuelve 429 con cabecera Retry-After.
    """

    def __init__(self, app):
        super().__init__(app)
        # Por IP: deque de timestamps (ventana deslizante).
        self._ventanas: dict[str, deque] = defaultdict(deque)
        self._auth_token = (
            settings.api_auth_token.get_secret_value()
            if settings.api_auth_token
            else None
        )

    @staticmethod
    def _const_eq(a: str, b: str) -> bool:
        """Comparación en tiempo constante (evita timing attacks)."""
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0

    def _ip_cliente(self, request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "desconocido"

    async def dispatch(self, request, call_next):
        clave_ruta = (request.url.path, request.method)
        if clave_ruta in _RUTAS_AGENTE:
            # 1) Auth (opt-in). Si está activa y la key es válida, se exime
            # del rate limit: confiamos en que el backend ya limita por
            # usuario. Sin key válida -> 401 (y nunca llega al rate limit).
            autenticado = False
            if self._auth_token:
                recibido = request.headers.get("x-api-key") or ""
                autenticado = self._const_eq(recibido, self._auth_token)
                if not autenticado:
                    return JSONResponse(
                        status_code=401,
                        content={
                            "error": "NO_AUTORIZADO",
                            "mensaje": "API key inválida o ausente.",
                        },
                    )

            # 2) Rate limit por IP, salvo clientes autenticados con la key
            # compartida (todo el tráfico del backend llega como una sola IP).
            if not autenticado:
                ip = self._ip_cliente(request)
                ahora = time.monotonic()
                ventana = self._ventanas[ip]
                limite = ahora - settings.rate_limit_window_seconds
                while ventana and ventana[0] < limite:
                    ventana.popleft()

                if len(ventana) >= settings.rate_limit_max_requests:
                    return JSONResponse(
                        status_code=429,
                        content={
                            "error": "DEMASIADAS_SOLICITUDES",
                            "mensaje": (
                                "Demasiadas consultas en poco tiempo. "
                                "Esperá unos segundos y reintentá."
                            ),
                        },
                        headers={"Retry-After": str(settings.rate_limit_window_seconds)},
                    )
                ventana.append(ahora)

        return await call_next(request)
