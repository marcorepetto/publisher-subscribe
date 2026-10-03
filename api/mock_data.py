from typing import Dict
from common.models import EarthquakeDetail

# Catálogo en memoria de sismos con datos reales / realistas de sismología chilena (sismologia.cl)
SAMPLE_EARTHQUAKES: Dict[str, EarthquakeDetail] = {
    "sismo-valparaiso-01": EarthquakeDetail(
        id="sismo-valparaiso-01",
        fecha_local="2026-10-03 14:22:10",
        fecha_utc="2026-10-03 17:22:10",
        latitud=-33.012,
        longitud=-71.745,
        profundidad_km=28.5,
        magnitud=5.4,
        escala="Mww",
        referencia_geografica="18 km al O de Valparaíso"
    ),
    "sismo-arica-01": EarthquakeDetail(
        id="sismo-arica-01",
        fecha_local="2026-10-03 09:15:40",
        fecha_utc="2026-10-03 12:15:40",
        latitud=-18.650,
        longitud=-70.420,
        profundidad_km=45.0,
        magnitud=6.1,
        escala="Mww",
        referencia_geografica="25 km al SO de Arica"
    ),
    "sismo-coquimbo-01": EarthquakeDetail(
        id="sismo-coquimbo-01",
        fecha_local="2026-10-03 11:05:12",
        fecha_utc="2026-10-03 14:05:12",
        latitud=-30.120,
        longitud=-71.450,
        profundidad_km=32.0,
        magnitud=4.8,
        escala="Ml",
        referencia_geografica="22 km al SO de Coquimbo"
    ),
    "sismo-concepcion-01": EarthquakeDetail(
        id="sismo-concepcion-01",
        fecha_local="2026-10-03 16:48:33",
        fecha_utc="2026-10-03 19:48:33",
        latitud=-36.750,
        longitud=-73.210,
        profundidad_km=21.0,
        magnitud=5.9,
        escala="Mww",
        referencia_geografica="20 km al NO de Concepción"
    ),
    "sismo-punta-arenas-01": EarthquakeDetail(
        id="sismo-punta-arenas-01",
        fecha_local="2026-10-03 04:30:00",
        fecha_utc="2026-10-03 07:30:00",
        latitud=-53.400,
        longitud=-71.100,
        profundidad_km=15.0,
        magnitud=4.5,
        escala="Ml",
        referencia_geografica="35 km al S de Punta Arenas"
    ),
    "sismo-antofagasta-01": EarthquakeDetail(
        id="sismo-antofagasta-01",
        fecha_local="2026-10-03 18:00:00",
        fecha_utc="2026-10-03 21:00:00",
        latitud=-23.650,
        longitud=-70.400,
        profundidad_km=50.0,
        magnitud=5.2,
        escala="Mww",
        referencia_geografica="30 km al N de Antofagasta"
    )
}
