import httpx
from app.core.config import settings

async def consultar_datos(
    filtros: dict,
    indicadores: list[str],
    agrupar_por: list[str] = ["cluster", "periodo"],
    idioma: str = "es"
) -> dict:
    """
    Llama a POST /datos del backend.
    Retorna datos estructurados por región e indicador.
    """
    payload = {
        "filtros": filtros,
        "indicadores": indicadores,
        "agrupar_por": agrupar_por,
        "idioma": idioma
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.backend_url}/datos",
                json=payload,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return { "error": str(e), "datos": [], "fuentes": [] }


async def consultar_brechas(
    servicio: str,
    municipio: str | None = None,
    periodo: str = "TARDE"
) -> dict:
    """
    Llama a GET /brechas del backend.
    Retorna zonas con demanda sin oferta para el servicio dado.
    """
    params = { "servicio": servicio, "periodo": periodo }
    if municipio:
        params["municipio"] = municipio

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.backend_url}/brechas",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return { "error": str(e), "brechas": [] }