from typing import Optional
from pydantic import BaseModel, Field

class MinimalEarthquakeEvent(BaseModel):
    """
    Mensaje mínimo transmitido a través del broker (AMQP).
    Contiene estrictamente lo necesario para que un suscriptor identifique el sismo
    y calcule la distancia geográfica para decidir si es de su interés.
    """
    id: str = Field(..., description="Identificador único del sismo")
    latitud: float = Field(..., description="Latitud del epicentro")
    longitud: float = Field(..., description="Longitud del epicentro")
    timestamp: Optional[str] = Field(default=None, description="Marca de tiempo de emisión del evento")

class EarthquakeDetail(BaseModel):
    """
    Ficha detallada del sismo entregada por el servicio HTTP (FastAPI),
    basada en la estructura oficial de sismologia.cl.
    """
    id: str = Field(..., description="Identificador único del sismo")
    fecha_local: str = Field(..., description="Fecha y hora local de ocurrencia")
    fecha_utc: str = Field(..., description="Fecha y hora UTC de ocurrencia")
    latitud: float = Field(..., description="Latitud del epicentro")
    longitud: float = Field(..., description="Longitud del epicentro")
    profundidad_km: float = Field(..., description="Profundidad en kilómetros")
    magnitud: float = Field(..., description="Magnitud del sismo")
    escala: str = Field(default="Mww", description="Escala de magnitud (ej. Mww, Ml)")
    referencia_geografica: str = Field(..., description="Referencia geográfica respecto a una localidad conocida")
