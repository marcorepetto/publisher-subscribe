from typing import Dict
from pydantic import BaseModel

class SubscriberLocation(BaseModel):
    name: str
    lat: float
    lon: float

# Coordenadas exactas solicitadas en el enunciado de la tarea
SUBSCRIBER_CITIES: Dict[str, SubscriberLocation] = {
    "arica": SubscriberLocation(
        name="Arica",
        lat=-18.4746,
        lon=-70.29792
    ),
    "coquimbo": SubscriberLocation(
        name="Coquimbo",
        lat=-29.95332,
        lon=-71.33947
    ),
    "valparaiso": SubscriberLocation(
        name="Valparaíso",
        lat=-33.036,
        lon=-71.62963
    ),
    "concepcion": SubscriberLocation(
        name="Concepción",
        lat=-36.82699,
        lon=-73.04977
    ),
    "punta_arenas": SubscriberLocation(
        name="Punta Arenas",
        lat=-53.16282,
        lon=-70.90922
    )
}

DISTANCE_THRESHOLD_KM = 500.0
