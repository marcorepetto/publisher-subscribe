import pytest
from common.models import MinimalEarthquakeEvent, EarthquakeDetail

def test_minimal_earthquake_event():
    event = MinimalEarthquakeEvent(
        id="test-sismo-01",
        latitud=-33.0,
        longitud=-71.0
    )
    dumped = event.model_dump()
    assert dumped["id"] == "test-sismo-01"
    assert dumped["latitud"] == -33.0
    assert dumped["longitud"] == -71.0
    
    # Comprobar que no incluye campos de datos pesados/detallados en el evento mínimo
    assert "profundidad_km" not in dumped
    assert "magnitud" not in dumped
    assert "referencia_geografica" not in dumped

def test_earthquake_detail_model():
    detail = EarthquakeDetail(
        id="test-detail-01",
        fecha_local="2026-10-03 12:00:00",
        fecha_utc="2026-10-03 15:00:00",
        latitud=-33.0,
        longitud=-71.0,
        profundidad_km=30.0,
        magnitud=5.5,
        escala="Mww",
        referencia_geografica="Valparaíso"
    )
    assert detail.magnitud == 5.5
    assert detail.escala == "Mww"
