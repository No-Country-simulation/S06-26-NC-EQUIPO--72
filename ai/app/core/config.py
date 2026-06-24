from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "mistralai/mistral-7b-instruct"
    backend_url: str = "http://backend:8080"
    
    # Variables de Qdrant (opcionales, no se usan por ahora)
    qdrant_url: str | None = None
    qdrant_collection: str | None = None
    
    # Configuración de BD MySQL
    db_host: str = "db"
    db_port: int = 3306
    db_name: str = "app_bit_b_2g_db"
    db_user: str = "root"
    db_password: str = "root"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False  # Permite variables en mayúsculas o minúsculas
    )

settings = Settings()