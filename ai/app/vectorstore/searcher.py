import logging
from google.generativeai import embed_content
from qdrant_client import QdrantClient
from app.core.config import settings
from app.vectorstore.indexer import get_qdrant_client

logger = logging.getLogger(__name__)



def search(query: str, top_k: int = 1) -> dict | None:
    """
    Busca el documento más similar a la consulta en Qdrant.
    Retorna el payload del mejor resultado si supera el umbral,
    o None si ninguno lo supera (-> fallback SQL).
    """
    threshold = settings.schema_linker_threshold
    result = embed_content(
        model=settings.gemini_embedding_model,
        content=query,
        task_type="RETRIEVAL_QUERY",
    )
    query_vector = result["embedding"]

    client = get_qdrant_client()
    hits = client.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    if not hits:
        return None

    best = hits[0]
    logger.info(
        "Schema linker: mejor match '%s' con score %.3f (umbral %.2f)",
        best.payload.get("id"),
        best.score,
        threshold,
    )

    if best.score < threshold:
        logger.info("Score por debajo del umbral — fallback a SQL.")
        return None

    return {**best.payload, "score": best.score}