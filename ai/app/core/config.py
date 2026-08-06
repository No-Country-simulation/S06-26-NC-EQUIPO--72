from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    # Groq
    groq_base_url: str = "https://api.groq.com/openai/v1"
    # llama-3.3-70b-versatile
    groq_api_key_primary: SecretStr
    # llama-3.1-8b-instant
    groq_api_key_light: SecretStr
    groq_model_primary: str = "llama-3.3-70b-versatile"
    groq_model_light: str = "llama-3.1-8b-instant"

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

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    schema_linker_threshold: float = 0.67



settings = Settings()