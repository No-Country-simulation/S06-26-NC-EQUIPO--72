import logging
from google import genai
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.vectorstore.indexer import get_qdrant_client, META_POINT_ID
from google.genai import types

logger = logging.getLogger(__name__)

client_genai = genai.Client(api_key=settings.google_api_key.get_secret_value())


def search(query: str, top_k: int = 1) -> dict | None:
    """
    Busca el documento más similar a la consulta en Qdrant.
    Retorna el payload del mejor resultado si supera el umbral,
    o None si ninguno lo supera (-> fallback SQL).
    """
    threshold = settings.schema_linker_threshold
    result = client_genai.models.embed_content(
        model=settings.gemini_embedding_model,
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query_vector = result.embeddings[0].values

    client = get_qdrant_client()

    # Filtrar para excluir el punto meta (no es un documento real, solo guarda el hash)
    filter_condition = Filter(
        must_not=[
            FieldCondition(key="type", match=MatchValue(value="meta"))
        ]
    )

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=filter_condition,  # <-- corregido: era "filter", no existe en query_points
    )

    hits = response.points

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