from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    # Groq
    groq_base_url: str = "https://api.groq.com/openai/v1"
    # openai/gpt-oss-120b (migrado post-deprecación 16/08/2026)
    groq_api_key_primary: SecretStr
    # groq/compound-mini (light) y openai/gpt-oss-120b (primary)
    groq_api_key_light: SecretStr
    # Cuenta Groq adicional (rotación): ante rate-limit TPM/TPD de la cuenta
    # principal, los nodos reutilizan la misma consulta con esta key antes
    # de degradar al fallback Gemini. Duplica el presupuesto diario free.
    groq_api_key_extra: SecretStr | None = None
    # Claves Groq adicionales para rotación (JSON array, ej.
    # GROQ_API_KEYS_ROTACION='["gsk_..","gsk_.."]'). Cada cuenta nueva suma
    # su cuota diaria de TPM/TPD al pool de rotación.
    groq_api_keys_rotacion: list[str] = Field(default_factory=list)
    groq_model_primary: str = "openai/gpt-oss-120b"
    groq_model_light: str = "groq/compound-mini"

    # Google (embeddings + fallback)
    google_api_key: SecretStr
    gemini_embedding_model: str = "gemini-embedding-001"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    gemini_model_fallback: str = "gemini-3.1-flash-lite"

    # Backend
    backend_url: str = "http://backend:8080/api"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: SecretStr | None = None
    qdrant_collection: str = "appbit"

    # MySQL
    db_host: str = "db"
    db_port: int = 3306
    db_name: str = "app_bit_b_2g_db"
    db_user: str = "root"
    db_password: SecretStr = SecretStr("root")
    
    # MySQL (usuario de solo lectura para Text-to-SQL)
    db_readonly_user: str = "ai_readonly"
    db_readonly_password: SecretStr = SecretStr("ai_readonly_pass")

    # LangSmith
    langsmith_api_key: SecretStr | None = None
    langsmith_project: str = "appbit-ai"
    langsmith_tracing: bool = False

    # Retry
    max_retries_llm: int = 2
    max_retries_tool: int = 2

    # DSPy compilado (sección 7.2 del plan). OFF por defecto: el nodo planner
    # usa compiled_modules/planner.json SOLO si existe el archivo Y este flag
    # está en True. Los evals de aceptación (golden + OOD, sin regresión) se
    # corren antes de habilitarlo; si regresan, se borra el archivo o se deja
    # False (revertir).
    dspy_compiled: bool = False

    # Ejecución acotada
    # recursion_limit 25: el límite 15 era justo al borde del peor caso
    # tras los loops de Fases 5-6 (ReAct + reflexion pueden ejecutar ~14
    # nodos + END). 25 deja margen sin riesgo de GraphRecursionError.
    agent_recursion_limit: int = 25
    agent_timeout_simple: float = 30.0
    # compuesta 60s: la consulta relacional tarda ~39s nominal (5 llamadas
    # LLM, 70B para classifier/decomposer). 30s cortaba consultas legítimas.
    agent_timeout_compuesta: float = 60.0

    # Formatter
    formatter_max_records: int = 8
    formatter_max_tokens_estimate: int = 3000

    # Reflexion
    reflector_min_quality_score: float = 0.6
    reflector_max_retries: int = 1

    # HITL — pausas de clarificación con el gestor
    hitl_session_ttl_seconds: int = 900  # 15 min entre pausa y reanudación
    hitl_cleanup_interval_seconds: int = 60

    # Seguridad de la API (auth + rate limit)
    # API key compartida con el backend: si está vacía/None la auth queda
    # DESHABILITADA (compatible con el backend actual que no envía header).
    # Para activarla: fijar AI_API_AUTH_TOKEN en .env y que el backend envíe
    # el header "X-API-Key". El valor del header se compara en tiempo
    # constante (secret-strcmp) para evitar timing attacks.
    api_auth_token: SecretStr | None = None
    # Rate limit por IP de cliente sobre POST /consulta y /consulta/respuesta.
    # Ventana deslizante en memoria (un solo worker). El AI Service solo
    # recibe tráfico del backend, así que un límite generoso basta para
    # frenar abuso directo al puerto 8000 sin cortar consultas legítimas.
    rate_limit_max_requests: int = 30
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    schema_linker_threshold: float = 0.68

    def claves_groq(self) -> list[str]:
        """Pool de claves Groq en orden de rotación (dedup, sin vacías).

        El runtime (graph.py) y el compile DSPy (dspy_config.py) comparten
        este pool: cada clave es una cuenta con su propia cuota diaria de
        TPM/TPD. Ante un 429 se rota a la siguiente clave antes de degradar
        al fallback Gemini.
        """
        claves = [self.groq_api_key_primary.get_secret_value(),
                  self.groq_api_key_light.get_secret_value()]
        if self.groq_api_key_extra:
            claves.append(self.groq_api_key_extra.get_secret_value())
        for k in self.groq_api_keys_rotacion:
            if k and k not in claves:
                claves.append(k)
        return claves



settings = Settings()