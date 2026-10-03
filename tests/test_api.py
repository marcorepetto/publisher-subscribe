import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["total_sismos_registrados"] > 0

def test_list_sismos():
    response = client.get("/sismos")
    assert response.status_code == 200
    sismos = response.json()
    assert isinstance(sismos, list)
    assert len(sismos) >= 5

def test_get_sismo_valparaiso():
    response = client.get("/sismos/sismo-valparaiso-01")
    assert response.status_code == 200
    sismo = response.json()
    assert sismo["id"] == "sismo-valparaiso-01"
    assert sismo["latitud"] == -33.012
    assert sismo["longitud"] == -71.745
    assert "referencia_geografica" in sismo
    assert "profundidad_km" in sismo
    assert "magnitud" in sismo

def test_get_sismo_not_found():
    response = client.get("/sismos/sismo-inexistente-999")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()
