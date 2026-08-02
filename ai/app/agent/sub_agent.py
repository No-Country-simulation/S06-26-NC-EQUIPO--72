import logging
from dataclasses import dataclass, field

from app.agent.tools import llamar_endpoint
from app.agent.schema_linker import _CATEGORIAS_VALIDAS_MAPA

logger = logging.getLogger(__name__)


@dataclass
class SubAgentResult:
    sub_agent_id: str
    endpoint: str
    results: list[dict] = field(default_factory=list)
    fuentes: list[dict] = field(default_factory=list)
    error: str | None = None
    records_count: int = 0

    def __post_init__(self):
        self.records_count = len(self.results)


async def run_sub_agent(sub_task: dict, request_id: str) -> SubAgentResult:
    """
    Ejecuta una sub-tarea: llama al endpoint y valida el resultado.
    Es una función async simple (NO un grafo LangGraph)- ver sección 2.2.
    Los errores transitorios del backend los reintenta llamar_endpoint
    (tenacity); los errores persistentes degradan a lista vacía con `error`.
    """
    sub_agent_id = sub_task["sub_agent_id"]
    endpoint = sub_task["endpoint"]
    params = sub_task.get("params", {})

    logger.info(
        "[%s] SUB_AGENT %s | endpoint=%s | params=%s",
        request_id, sub_agent_id, endpoint, params
    )

    # Guarda determinística: /mapa/indicadores solo acepta categorias válidas
    # (SALUD_MENTAL/EMPLEO/EDUCACION). Evita llamadas 400 al backend y
    # resultados vacíos engañosos (ver Fix Bug E).
    if endpoint == "/mapa/indicadores":
        categoria = params.get("categoria")
        if categoria and categoria not in _CATEGORIAS_VALIDAS_MAPA:
            logger.warning(
                "[%s] SUB_AGENT %s | categoria '%s' inválida para "
                "/mapa/indicadores- omitiendo",
                request_id, sub_agent_id, categoria
            )
            return SubAgentResult(
                sub_agent_id=sub_agent_id,
                endpoint=endpoint,
                results=[],
                fuentes=[],
                error=f"categoria '{categoria}' inválida para /mapa/indicadores",
            )

    try:
        data = await llamar_endpoint(
            metodo="GET",
            endpoint=endpoint,
            params=params,
            request_id=request_id,
        )
        results = data.get("resultado", [])
        fuentes = data.get("fuentes", [])

        # Contrato: resultados siempre list[dict]
        if isinstance(results, dict):
            results = [results] if results else []
        elif not isinstance(results, list):
            results = []

        logger.info(
            "[%s] SUB_AGENT %s | records=%d",
            request_id, sub_agent_id, len(results)
        )

        return SubAgentResult(
            sub_agent_id=sub_agent_id,
            endpoint=endpoint,
            results=results,
            fuentes=fuentes,
        )

    except Exception as e:
        logger.error(
            "[%s] SUB_AGENT %s error: %s", request_id, sub_agent_id, e
        )
        return SubAgentResult(
            sub_agent_id=sub_agent_id,
            endpoint=endpoint,
            results=[],
            fuentes=[],
            error=str(e),
        )
