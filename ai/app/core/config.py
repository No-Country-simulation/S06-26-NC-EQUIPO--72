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
    gemini_embedding_model: str = "models/gemini-embedding-exp-03-07"
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    gemini_model_fallback: str = "gemini-2.0-flash-lite"

    # Backend
    backend_url: str = "http://backend:8080"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection: str = "appbit"

    # MySQL
    db_host: str = "db"
    db_port: int = 3306
    db_name: str = "app_bit_b_2g_db"
    db_user: str = "root"
    db_password: SecretStr = SecretStr("root")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    schema_linker_threshold: float = 0.70



settings = Settings()