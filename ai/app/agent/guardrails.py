import logging
import re

from app.agent.state import AgentState, get_tool_results

logger = logging.getLogger(__name__)


# Patrones de inyección directa. Capa de input, NO la única barrera:
# OWASP es explícito en que el filtrado de input no puede prevenir todo. La
# defensa real está en la separación estructural y las allowlists.
_PATRONES_INYECCION = (
    r"ignora?\s+(todas\s+)?(las\s+)?instrucciones",
    r"ignore\s+(all\s+)?(previous\s+)?instructions?",
    r"developer\s+mode|modo\s+desarrollador",
    r"reveal\s+(your\s+)?(system\s+)?prompt|mostr[áa]\s+las\s+instrucciones",
    r"system\s+prompt",
    r"override|sobreescribe|sobrescrib[ií]",
    r"repet[ií]\s+el\s+texto\s+anterior|repeat\s+everything\s+above",
    r"you\s+are\s+now|eres\s+ahora|act[uú]a\s+como|pretende\s+ser",
    r"disregard|desobedec[eé]|ignora\s+las\s+reglas",
    r"what\s+were\s+your\s+exact\s+instructions",
)

# Palabras clave para detección fuzzy (typoglycemia: letras internas
# desordenadas como "ignroe" en vez de "ignore"). Se compara por distancia
# de edición contra cada palabra de la consulta (mismo patrón que normalizer).
_PALABRAS_RIESGO = (
    "ignore", "ignora", "instrucciones", "instructions", "prompt",
    "override", "reveal", "system", "developer", "delete", "bypass",
)

_MAX_RESPUESTA_GESTOR = 500

# --- Checks de output (zero-trust) ---
# Si el formatter fue manipulado por inyección, la respuesta puede contener
# fugas del system prompt, credenciales, o exfiltración vía markup/imágenes.
_PATRONES_FUGA_RESPUESTA = (
    r"api[_\-\s]?key[\s:=]+\S{8,}",
    r"secret[\s:=]+\S{8,}",
    r"password[\s:=]+\S{8,}",
    r"sk-[A-Za-z0-9]{10,}",
    r"AIza[0-9A-Za-z_-]{20,}",           # Google API key
    r"gsk_[A-Za-z0-9]{10,}",              # Groq API key
    r"<img[^>]+src=[\"']http",
    r"\[!\[[^\]]*\]\(http",
    r"https?://[^\s<>\"']{25,}",          # URL externa sospechosa
)


def _detectar_fuga_respuesta(respuesta: str) -> str | None:
    """Detecta fugas de información sensible en la respuesta del LLM."""
    if not isinstance(respuesta, str) or not respuesta:
        return None
    lower = respuesta.lower()
    for patron in _PATRONES_FUGA_RESPUESTA:
        if re.search(patron, lower, re.IGNORECASE):
            return f"fuga potencial en respuesta: {patron}"
    # Base64 largo en la respuesta (exfiltración ofuscada)
    compacto = re.sub(r"\s+", "", respuesta)
    if len(compacto) >= 64 and re.fullmatch(r"[A-Za-z0-9+/=]+", compacto):
        return "respuesta con bloque base64 sospechoso"
    return None


def _es_parecida(palabra: str, objetivo: str) -> bool:
    """True si la palabra es una variante tipográfica/typoglycemia de `objetivo`."""
    if palabra == objetivo:
        return True
    if len(palabra) != len(objetivo) or len(palabra) < 3:
        return False
    # Misma primera y última letra, interior desordenado (typoglycemia)
    return (
        palabra[0] == objetivo[0]
        and palabra[-1] == objetivo[-1]
        and sorted(palabra[1:-1]) == sorted(objetivo[1:-1])
    )


def _detectar_inyeccion(texto: str) -> str | None:
    """
    Detecta señales de prompt injection en un texto. Devuelve la razón de
    detección (str) o None si no hay señales. Determinística, sin LLM.
    """
    if not isinstance(texto, str) or not texto.strip():
        return None
    lower = texto.lower()

    # 1. Patrones explícitos (regex)
    for patron in _PATRONES_INYECCION:
        if re.search(patron, lower):
            return f"patrón sospechoso: {patron}"

    # 2. Base64 largo (posible instrucción ofuscada)
    compacto = re.sub(r"\s+", "", texto)
    if len(compacto) >= 40 and re.fullmatch(r"[A-Za-z0-9+/=\n]+", compacto):
        if len(compacto) % 4 == 0 and "=" in compacto:
            return "posible contenido base64"

    # 3. Typoglycemia (fuzzy) sobre palabras de riesgo
    palabras = re.findall(r"[a-záéíóúñçãõ]{4,}", lower)
    for palabra in palabras:
        for objetivo in _PALABRAS_RIESGO:
            if _es_parecida(palabra, objetivo):
                return f"palabra de riesgo (variante): {palabra}"
    return None


def _sanitizar_consulta(consulta: str) -> str:
    """
    Sanitización de input: limita a 500 chars y elimina
    caracteres de control (salvo \n y \t). Sin LLM- rápido y barato.
    """
    MAX_CHARS = 500
    if len(consulta) > MAX_CHARS:
        logger.warning("Consulta truncada de %d a %d chars", len(consulta), MAX_CHARS)
        consulta = consulta[:MAX_CHARS]
    # Eliminar caracteres de control excepto salto de línea y tab
    consulta = "".join(c for c in consulta if c.isprintable() or c in ("\n", "\t"))
    return consulta.strip()


def _sanitizar_respuesta_gestor(respuesta: str) -> str:
    """Sanitiza la respuesta del gestor (canal HITL): trunca y limpia."""
    if not isinstance(respuesta, str):
        return ""
    respuesta = _sanitizar_consulta(respuesta)
    return respuesta[: _MAX_RESPUESTA_GESTOR]


async def input_guardrail(state: AgentState) -> AgentState:
    """
    Validación determinística de la consulta antes de procesarla.
    Sin LLM- rápido y barato. Si la consulta es inválida o tiene señales de
    prompt injection, corta el flujo (el router lo lleva a END).
    """
    consulta = state.get("consulta", "")

    # Consulta vacía o demasiado corta
    if len(consulta.strip()) < 3:
        return {
            **state,
            "fuera_de_dominio": True,
            "respuesta_ia": "La consulta está vacía o es demasiado corta.",
        }

    # Detección de prompt injection
    razon = _detectar_inyeccion(consulta)
    if razon:
        logger.warning(
            "[%s] INPUT_GUARDRAIL | posible prompt injection: %s",
            state.get("request_id", "-"), razon,
        )
        return {
            **state,
            "fuera_de_dominio": True,
            "flag_inyeccion": razon,
            "respuesta_ia": (
                "No puedo procesar esa solicitud por razones de seguridad."
            ),
        }

    # Sanitización
    consulta_sanitizada = _sanitizar_consulta(consulta)

    return {**state, "consulta": consulta_sanitizada}


async def output_guardrail(state: AgentState) -> AgentState:
    """
    Validación de coherencia entre consulta y datos obtenidos.
    Sin LLM- determinístico. Registra advertencias en tool_results_meta
    y calcula datos_validos (True si no hay advertencias salvo "resultado vacío").
    """
    tool_results = get_tool_results(state)
    merged = state.get("merged_results", [])
    datos = merged or tool_results
    decision = state.get("schema_decision", {})
    advertencias = []

    # Check 1: datos vacíos
    if not datos:
        advertencias.append("resultado vacío")

    # Check 2: error en tool caller
    if state.get("tool_error"):
        advertencias.append(f"tool_error: {state['tool_error']}")

    # Check 3: /brechas sin severidad_brecha
    if decision.get("endpoint") == "/brechas" and datos:
        if not any("severidad_brecha" in r for r in datos):
            advertencias.append("/brechas sin campo severidad_brecha")

    # Check 4: sub-agentes con error en consulta compuesta
    for sr in state.get("sub_agent_results", []):
        if sr.get("error"):
            advertencias.append(f"sub_agent {sr['sub_agent_id']}: {sr['error']}")

    # Check 5: fuga de información sensible en la respuesta
    fuga = _detectar_fuga_respuesta(state.get("respuesta_ia", ""))
    if fuga:
        logger.warning(
            "[%s] OUTPUT_GUARDRAIL | %s",
            state.get("request_id", "-"), fuga,
        )
        advertencias.append(f"respuesta_ia: {fuga}")
        # Reemplazar la respuesta por una genérica- nunca entregar contenido
        # con credenciales, markup de exfiltración o fugas del system prompt.
        state = {
            **state,
            "respuesta_ia": (
                "No puedo mostrar la respuesta por razones de seguridad."
            ),
            "flag_inyeccion": "fuga detectada en respuesta",
        }

    if advertencias:
        logger.warning(
            "[%s] OUTPUT_GUARDRAIL | advertencias: %s",
            state.get("request_id", "-"), "; ".join(advertencias)
        )

    return {
        **state,
        "datos_validos": not bool([a for a in advertencias if "vacío" not in a]),
        "tool_results_meta": {
            **state.get("tool_results_meta", {}),
            "advertencias": advertencias,
        },
    }
