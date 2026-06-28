import logging
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google.generativeai import embed_content
from app.core.config import settings
from app.vectorstore.documents import ALL_DOCUMENTS
import google.generativeai as genai

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.google_api_key.get_secret_value())


COLLECTION_NAME = settings.qdrant_collection
VECTOR_SIZE = 768  # dimensión de gemini-embedding-exp-03-07


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def _embed(text: str) -> list[float]:
    result = embed_content(
        model=settings.gemini_embedding_model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return result["embedding"]


def init_vectorstore() -> None:
    """
    Inicializa la colección en Qdrant e indexa los documentos.
    Se llama una vez al startup. Si la colección ya existe y tiene
    el mismo número de puntos, omite la re-indexación.
    """
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in existing:
        info = client.get_collection(COLLECTION_NAME)
        if info.points_count == len(ALL_DOCUMENTS):
            logger.info(
                "Vectorstore ya inicializado con %d documentos - omitiendo re-indexación.",
                len(ALL_DOCUMENTS),
            )
            return
        logger.info("Colección existente con distinto número de puntos - re-indexando.")
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
    )

    points = []
    for i, doc in enumerate(ALL_DOCUMENTS):
        vector = _embed(doc["texto"])
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={k: v for k, v in doc.items() if k != "texto"},
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logger.info("Vectorstore inicializado con %d documentos.", len(ALL_DOCUMENTS))