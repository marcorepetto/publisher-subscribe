import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import List, Dict
from fastapi import FastAPI, HTTPException, status
from common.models import EarthquakeDetail
from api.mock_data import SAMPLE_EARTHQUAKES

app = FastAPI(
    title="Servicio HTTP de Datos de Sismos - INF-326",
    description="Servicio REST para consultar información detallada de eventos sísmicos (Modelo Pull).",
    version="1.0.0"
)

# Almacenamiento en memoria para los sismos
earthquakes_db: Dict[str, EarthquakeDetail] = dict(SAMPLE_EARTHQUAKES)

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint para verificar disponibilidad del servicio HTTP."""
    return {"status": "ok", "total_sismos_registrados": len(earthquakes_db)}

@app.get("/sismos", response_model=List[EarthquakeDetail], tags=["Sismos"])
def list_sismos():
    """Obtiene el listado completo de sismos registrados en el catálogo."""
    return list(earthquakes_db.values())

@app.get("/sismos/{sismo_id}", response_model=EarthquakeDetail, tags=["Sismos"])
def get_sismo(sismo_id: str):
    """
    Obtiene la ficha técnica detallada de un sismo dado su identificador único.
    Utilizado por los suscriptores cuando determinan que el evento es de su interés (< 500 km).
    """
    if sismo_id not in earthquakes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sismo con ID '{sismo_id}' no encontrado en el registro."
        )
    return earthquakes_db[sismo_id]

@app.post("/sismos", response_model=EarthquakeDetail, status_code=status.HTTP_201_CREATED, tags=["Sismos"])
def register_sismo(sismo: EarthquakeDetail):
    """
    Permite registrar o actualizar dinámicamente un sismo en el catálogo en memoria
    (opcional para facilitar pruebas personalizadas).
    """
    earthquakes_db[sismo.id] = sismo
    return sismo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
