from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "mistralai/mistral-7b-instruct"
    backend_url: str = "http://localhost:3000"
    
    # Variables de Qdrant (opcionales, no se usan por ahora)
    qdrant_url: str | None = None
    qdrant_collection: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False  # Permite variables en mayúsculas o minúsculas
    )

settings = Settings()