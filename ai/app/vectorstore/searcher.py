import logging
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.vectorstore.indexer import get_qdrant_client, META_POINT_ID
from google.genai import types

logger = logging.getLogger(__name__)

client_genai = genai.Client(api_key=settings.google_api_key.get_secret_value())


def search(query: str, top_k: int = 1, tipo: str | None = None, debug: bool = False) -> dict | None:
    """
    Busca el documento más similar a la consulta en Qdrant.
    Si `tipo` se especifica ("endpoint" o "sql"), restringe la búsqueda
    a documentos de ese tipo únicamente.
    Retorna el payload del mejor resultado si supera el umbral,
    o None si ninguno lo supera (-> fallback).
    """
    threshold = settings.schema_linker_threshold
    result = client_genai.models.embed_content(
        model=settings.gemini_embedding_model,
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query_vector = result.embeddings[0].values

    client = get_qdrant_client()

    must_not = [FieldCondition(key="type", match=MatchValue(value="meta"))]
    must = []
    if tipo:
        must.append(FieldCondition(key="tipo", match=MatchValue(value=tipo)))

    filter_condition = Filter(must=must or None, must_not=must_not)

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=filter_condition,
    )

    hits = response.points

    if not hits:
        logger.info("Sin resultados en Qdrant para tipo=%s", tipo)
        return None

    best = hits[0]
    logger.info(
        "Schema linker [tipo=%s]: mejor match '%s' con score %.4f (umbral %.2f)",
        tipo, best.payload.get("id"), best.score, threshold,
    )

    if best.score < threshold and not debug:
        logger.info("Score por debajo del umbral — descartado (tipo=%s).", tipo)
        return None

    return {**best.payload, "score": best.score, "paso_umbral": best.score >= threshold} 