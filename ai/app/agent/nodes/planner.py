import asyncio
import json
import logging
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.exceptions import OutputParserException
from pydantic import ValidationError

from app.agent.prompts import PLANNER_PROMPT
from app.agent.state import AgentState
from app.agent.retry import llm_retry
from app.agent.parsing import _extraer_json_con_fallback
from app.agent.json_utils import json_default
from app.agent.normalizer import normalizar_plan
from app.agent.security import envolver_consulta
from app.agent.llm_layer import (
    _llm_ainvoke_con_fallback,
    _planner_models,
    _planner_fallback_model,
    _light_models,
    _fallback_model,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


def _parse_bool(val) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).lower() in ("true", "1", "yes")


def _parse_nullable(val):
    if val is None or str(val).lower() in ("null", "none", ""):
        return None
    return str(val)


def _run_dspy_async(module, **kwargs):
    """Wrapper async para módulos DSPy (corre forward sync en el executor)."""
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, lambda: module(**kwargs))


async def _plan_via_dspy(state: AgentState):
    """Corre el planner con el módulo DSPy compilado si existe y está habilitado.

    Devuelve el plan normalizado, o None si no está habilitado (settings.
    dspy_compiled) o no hay módulo compilado en disco. La importación de DSPy
    es perezosa (no forzar la dependencia al arrancar).
    """
    if not settings.dspy_compiled:
        return None
    path = Path("compiled_modules") / "planner.json"
    if not path.exists():
        return None

    from app.agent import dspy_modules as _dspy_mod
    _dspy_mod.init_modules(use_compiled=True)
    consulta = state["consulta"]
    resultado = await _run_dspy_async(_dspy_mod.planner_module, consulta=consulta)
    return _plan_desde_prediccion(resultado, state)


def _plan_desde_prediccion(resultado, state: AgentState) -> dict:
    plan = {
        "fuera_de_dominio": _parse_bool(getattr(resultado, "fuera_de_dominio", False)),
        "servicio": _parse_nullable(getattr(resultado, "servicio", None)),
        "municipio": _parse_nullable(getattr(resultado, "municipio", None)),
        "cluster": _parse_nullable(getattr(resultado, "cluster", None)),
        "indicador": _parse_nullable(getattr(resultado, "indicador", None)),
        "periodo": _parse_nullable(getattr(resultado, "periodo", None)),
        "income_cluster": _parse_nullable(getattr(resultado, "income_cluster", None)),
        "fecha": _parse_nullable(getattr(resultado, "fecha", None)),
        "razon": getattr(resultado, "razon", "") or "",
    }
    return normalizar_plan(plan, state["consulta"])


@llm_retry(max_attempts=settings.max_retries_llm + 1)
async def planner(state: AgentState) -> AgentState:
    request_id = state.get("request_id", "-")
    try:
        plan = await _plan_via_dspy(state)
        if plan is not None:
            logger.info("[%s] PLANNER | via DSPy compilado | servicio=%s | municipio=%s | fuera_dominio=%s",
                        request_id, plan.get("servicio"), plan.get("municipio"),
                        plan.get("fuera_de_dominio"))
            return {**state, "plan": plan}
    except Exception as e:
        logger.warning("[%s] PLANNER | error en módulo DSPy (%s) - usando infra ChatOpenAI",
                       request_id, e)
    try:
        # Structured output: Pydantic valida el JSON y elimina el parsing manual.
        result = await _llm_ainvoke_con_fallback(
            _planner_models, _planner_fallback_model,
            [
                SystemMessage(content=PLANNER_PROMPT),
                HumanMessage(content=envolver_consulta(state["consulta"]))
            ],
            request_id, "PLANNER",
        )
        plan = result.model_dump()
    except (OutputParserException, ValidationError, json.JSONDecodeError) as e:
        # Fallback: el modelo no produjo JSON válido- reintentar parseo manual.
        # Los errores transitorios de API los reintenta el decorador @llm_retry.
        logger.warning("[%s] PLANNER | structured output falló: %s- fallback manual",
                       request_id, e)
        response = await _llm_ainvoke_con_fallback(
            _light_models, _fallback_model,
            [
                SystemMessage(content=PLANNER_PROMPT),
                HumanMessage(content=envolver_consulta(state["consulta"]))
            ],
            request_id, "PLANNER",
        )
        plan = _extraer_json_con_fallback(response.content, request_id)
    plan = normalizar_plan(plan, state["consulta"])  # <-- corrección determinística post-LLM

    logger.info("[%s] PLANNER | servicio=%s | municipio=%s | fuera_dominio=%s",
                request_id, plan.get("servicio"), plan.get("municipio"),
                plan.get("fuera_de_dominio"))
    logger.debug("[%s] PLANNER | plan=%s", request_id,
                 json.dumps(plan, ensure_ascii=False, default=json_default))

    return {**state, "plan": plan}
