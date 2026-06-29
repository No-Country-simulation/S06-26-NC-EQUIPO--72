import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

def get_database_url():
    return f"mysql+mysqlconnector://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def wait_for_database(max_retries: int = 30, retry_interval: int = 2):
    retries = 0
    while retries < max_retries:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB lista", flush=True)
            return True
        except Exception as e:
            print(f"DB no lista. Intentando conectar en {retry_interval} segundos... (Error: {str(e)})", flush=True)

            time.sleep(retry_interval)
            retries += 1
    raise Exception(f"DB no lista después de {max_retries} intentos")
