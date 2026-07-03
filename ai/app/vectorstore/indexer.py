import logging
import json
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from google import genai
from google.genai import types
from app.core.config import settings
from app.vectorstore.documents import ALL_DOCUMENTS

logger = logging.getLogger(__name__)

client_genai = genai.Client(api_key=settings.google_api_key.get_secret_value())

COLLECTION_NAME = settings.qdrant_collection

# Qdrant exige IDs enteros sin signo o UUID — un string arbitrario como "__meta__"
# hace fallar el upsert con un error de validación. Usamos un UUID fijo y reservado.
META_POINT_ID = "00000000-0000-0000-0000-000000000000"

# task_type usado al indexar documentos. Se centraliza acá para que el hash
# de invalidación lo tenga en cuenta automáticamente.
_EMBEDDING_TASK_TYPE = "RETRIEVAL_DOCUMENT"


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)


def _embed(text: str) -> list[float]:
    result = client_genai.models.embed_content(
        model=settings.gemini_embedding_model,
        contents=text,
        config=types.EmbedContentConfig(task_type=_EMBEDDING_TASK_TYPE),
    )
    return result.embeddings[0].values


def _documents_hash() -> str:
    """
    Hash del contenido + modelo de embedding + task_type, para invalidar
    el cache automáticamente cuando cualquiera de los tres cambie.
    """
    raw = json.dumps(
        [(d["id"], d["texto"]) for d in ALL_DOCUMENTS],
        ensure_ascii=False,
    ) + settings.gemini_embedding_model + _EMBEDDING_TASK_TYPE
    return hashlib.sha256(raw.encode()).hexdigest()


def _get_stored_hash(client: QdrantClient) -> str | None:
    """Obtiene el hash almacenado en la colección (si existe)."""
    try:
        # Intentar recuperar el punto meta
        points = client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[META_POINT_ID],
            with_payload=True,
            with_vectors=False,
        )
        if points and len(points) > 0:
            return points[0].payload.get("hash")
    except Exception:
        # El punto meta no existe o la colección no existe
        pass
    return None


def init_vectorstore() -> None:
    """
    Inicializa la colección en Qdrant e indexa los documentos.
    Usa un hash de los documentos + config de embedding para invalidar automáticamente.
    """
    current_hash = _documents_hash()
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME in existing:
        stored_hash = _get_stored_hash(client)
        if stored_hash == current_hash:
            logger.info(
                "Vectorstore ya inicializado y sin cambios - omitiendo re-indexación.",
            )
            return
        logger.info(
            "Vectorstore desactualizado (hash distinto) - re-indexando."
        )
        client.delete_collection(COLLECTION_NAME)

    # Generar todos los puntos primero para conocer el tamaño del vector
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

    vector_size = len(points[0].vector) if points else 0

    # Crear la colección
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    # Agregar el punto meta con el hash
    # Usamos un vector de ceros para el punto meta (no participará en búsquedas
    # relevantes ya que searcher.py lo excluye explícitamente por filtro)
    meta_vector = [0.0] * vector_size if vector_size > 0 else []
    points.append(
        PointStruct(
            id=META_POINT_ID,
            vector=meta_vector,
            payload={"hash": current_hash, "type": "meta"},
        )
    )

    # Insertar todos los puntos
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logger.info(
        "Vectorstore inicializado con %d documentos y hash %s.",
        len(ALL_DOCUMENTS),
        current_hash[:12],  # Mostrar solo los primeros 12 chars para brevedad
    )