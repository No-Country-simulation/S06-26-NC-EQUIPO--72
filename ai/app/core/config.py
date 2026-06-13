from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "mistralai/mistral-7b-instruct"
    backend_url: str = "http://localhost:3000"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "appbit"

    class Config:
        env_file = ".env"

settings = Settings()