from app.core.config import settings
from app.agent.resumir import _necesita_resumen, resumir_para_formatter


def _record(**extra):
    base = {"cluster": "C1", "municipio": "São José"}
    base.update(extra)
    return base


def test_dataset_pequeno_no_se_resume():
    datos = [_record(cluster=f"C{i}") for i in range(4)]
    resultado, fue = resumir_para_formatter(datos)
    assert fue is False
    assert resultado == datos


def test_dataset_grande_sin_brecha_resume_con_muestra():
    datos = [_record(cluster=f"C{i}", campo_largo="x" * 200) for i in range(60)]
    resultado, fue = resumir_para_formatter(datos)
    assert fue is True
    assert resultado["total_zonas"] == 60
    assert len(resultado["muestra"]) == settings.formatter_max_records
    assert "mostrando" in resultado["nota"]


def test_dataset_grande_con_brecha_resume_por_severidad():
    datos = [
        _record(
            cluster=f"C{i}",
            severidad_brecha=("ALTA" if i % 2 == 0 else "MEDIA"),
            campo_largo="y" * 200,
        )
        for i in range(60)
    ]
    resultado, fue = resumir_para_formatter(datos)
    assert fue is True
    assert resultado["total_zonas"] == 60
    assert all(r["severidad_brecha"] == "ALTA" for r in resultado["zonas_alta_prioridad"])
    assert resultado["media_count"] == 30
    assert resultado["baja_count"] == 0


def test_dataset_vacio_no_resume():
    resultado, fue = resumir_para_formatter([])
    assert fue is False
    assert resultado == []


def test_necesita_resumen_umbral():
    assert _necesita_resumen([_record(cluster="C1")], 1000) is False
    assert _necesita_resumen([_record(cluster="C1", campo="x" * 5000)], 1000) is True
