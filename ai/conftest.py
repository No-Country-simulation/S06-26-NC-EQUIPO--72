# Raíz del paquete app- pytest agrega este dir al sys.path (import mode prepend).

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from app.agent.graph import build_graph


@pytest.fixture
def test_agent():
    """Agente con checkpointer aislado para tests (Corrección 4).

    Cada test usa su propio InMemorySaver: los checkpoints acumulados no
    tocan el `_checkpointer` global de producción ni los de otros tests.
    """
    checkpointer = InMemorySaver()
    return build_graph(checkpointer=checkpointer)
