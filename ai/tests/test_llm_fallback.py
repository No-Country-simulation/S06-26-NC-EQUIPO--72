import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from openai import RateLimitError

from app.agent.graph import _llm_ainvoke_con_fallback
from app.agent.tools import ejecutar_sql


def _rate_limit(msg: str) -> RateLimitError:
    request = httpx.Request("POST", "https://api.groq.com/openai/v1")
    response = httpx.Response(status_code=429, request=request)
    return RateLimitError(
        message=msg,
        response=response,
        body={"error": {"type": "tokens"}},
    )


class _FakeModel:
    def __init__(self, respuestas, name="fake"):
        self.respuestas = list(respuestas)
        self.llamadas = 0
        self.model_name = name

    async def ainvoke(self, mensajes):
        self.llamadas += 1
        r = self.respuestas.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def test_sin_rate_limit_no_usa_fallback():
    principal = _FakeModel(["respuesta_ok"])
    fallback = _FakeModel(["fallback_usado"])
    result = asyncio.run(_llm_ainvoke_con_fallback(
        principal, fallback, [object()], "r1", "PLANNER"))
    assert result == "respuesta_ok"
    assert principal.llamadas == 1
    assert fallback.llamadas == 0


def test_rate_limit_cambia_al_fallback():
    principal = _FakeModel([_rate_limit("429 TPM")])
    fallback = _FakeModel(["respuesta_del_fallback"])
    result = asyncio.run(_llm_ainvoke_con_fallback(
        principal, fallback, [object()], "r2", "PLANNER"))
    assert result == "respuesta_del_fallback"
    assert principal.llamadas == 1
    assert fallback.llamadas == 1


def test_si_ambos_fallan_propaga():
    principal = _FakeModel([_rate_limit("429 principal")])
    fallback = _FakeModel([_rate_limit("429 fallback")])
    try:
        asyncio.run(_llm_ainvoke_con_fallback(
            principal, fallback, [object()], "r3", "FORMATTER"))
        raise AssertionError("debió propagar RateLimitError")
    except RateLimitError:
        pass


def _mock_db(rows):
    cur = MagicMock()
    cur.__aenter__ = AsyncMock(return_value=cur)
    cur.execute = AsyncMock()
    cur.fetchall = AsyncMock(return_value=rows)
    conn = MagicMock()
    conn.__aenter__ = AsyncMock(return_value=conn)
    conn.cursor = MagicMock(return_value=cur)
    conn.close = MagicMock()
    return patch("app.agent.tools.aiomysql.connect", AsyncMock(return_value=conn))


def test_sql_rate_limit_usa_fallback():
    principal = _FakeModel([_rate_limit("429 TPM")], name="70b")
    fallback = _FakeModel([MagicMock(content="SELECT 1 FROM dual LIMIT 1")], name="8b")
    with _mock_db([{"a": 1}]):
        result = asyncio.run(ejecutar_sql(
            consulta="dato", schema_minimo="tabla", model=principal,
            model_fallback=fallback, request_id="r4"))
    assert result["resultado"] == [{"a": 1}]
    assert principal.llamadas == 1
    assert fallback.llamadas == 1


def _mock_db_con_sql(rows):
    """Igual que _mock_db pero captura el SQL ejecutado."""
    cur = MagicMock()
    cur.__aenter__ = AsyncMock(return_value=cur)
    cur.execute = AsyncMock()
    cur.fetchall = AsyncMock(return_value=rows)
    conn = MagicMock()
    conn.__aenter__ = AsyncMock(return_value=conn)
    conn.cursor = MagicMock(return_value=cur)
    conn.close = MagicMock()
    patcher = patch("app.agent.tools.aiomysql.connect", AsyncMock(return_value=conn))
    return patcher, cur


def test_sql_full_scan_inserta_where_antes_de_limit():
    modelo = _FakeModel([
        MagicMock(content="SELECT * FROM concentracao LIMIT 50")
    ], name="8b")
    patcher, cur = _mock_db_con_sql([{"region": "x"}])
    with patcher:
        result = asyncio.run(ejecutar_sql(
            consulta="dato", schema_minimo="tabla concentracao",
            model=modelo, request_id="r5"))
    assert result["resultado"] == [{"region": "x"}]
    sql = cur.execute.await_args.args[0]
    assert "WHERE concentracao.day_date" in sql
    assert sql.index("WHERE") < sql.index("LIMIT")


def test_sql_full_scan_con_limit_en_salto_de_linea():
    # El modelo real emite "LIMIT\n50" (o LIMIT;50). El guard debe insertar el
    # WHERE antes del LIMIT igual- el fix " limit " con espacios no lo matcheaba
    # y agregaba el WHERE DESPUÉS del LIMIT -> syntax error 1064 (eval_028).
    modelo = _FakeModel([
        MagicMock(content="SELECT * FROM concentracao AS c\nLIMIT\n50;")
    ], name="8b")
    patcher, cur = _mock_db_con_sql([{"x": 1}])
    with patcher:
        result = asyncio.run(ejecutar_sql(
            consulta="dato", schema_minimo="tabla concentracao",
            model=modelo, request_id="r6"))
    assert result["resultado"] == [{"x": 1}]
    sql = cur.execute.await_args.args[0]
    assert sql.index("WHERE") < sql.index("LIMIT")
    assert "WHERE concentracao.day_date" in sql
    assert sql.rstrip().endswith("50")


def test_sql_con_where_y_day_date_no_duplica_filtro():
    # Bug eval_028: el guard comparaba "where" (minúscula) contra sql_upper
    # (MAYÚSCULA) -> nunca matcheaba -> disparaba SIEMPRE y duplicaba el filtro
    # de fecha -> syntax error 1064. Con WHERE + day_date el guard NO debe tocar nada.
    modelo = _FakeModel([
        MagicMock(content="SELECT * FROM concentracao\nWHERE cluster = 'X'\nAND day_date = (SELECT MAX(day_date) FROM concentracao)")
    ], name="8b")
    patcher, cur = _mock_db_con_sql([{"x": 1}])
    with patcher:
        result = asyncio.run(ejecutar_sql(
            consulta="dato", schema_minimo="tabla concentracao",
            model=modelo, request_id="r7"))
    assert result["resultado"] == [{"x": 1}]
    sql = cur.execute.await_args.args[0]
    assert sql.count("WHERE") == 1
    assert sql.count("MAX(day_date)") == 1


def test_sql_con_where_sin_day_date_agrega_and():
    # WHERE presente pero sin filtro de day_date -> el guard agrega " AND day_date"
    # antes del LIMIT (no duplica el WHERE).
    modelo = _FakeModel([
        MagicMock(content="SELECT * FROM concentracao\nWHERE cluster = 'X'\nLIMIT 50")
    ], name="8b")
    patcher, cur = _mock_db_con_sql([{"x": 1}])
    with patcher:
        result = asyncio.run(ejecutar_sql(
            consulta="dato", schema_minimo="tabla concentracao",
            model=modelo, request_id="r8"))
    assert result["resultado"] == [{"x": 1}]
    sql = cur.execute.await_args.args[0]
    assert sql.count("WHERE") == 1
    assert "AND concentracao.day_date" in sql
    assert sql.index("AND") < sql.index("LIMIT")
