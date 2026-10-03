import pytest
from common.distance import calculate_geodesic_distance
from common.subscribers_config import SUBSCRIBER_CITIES, DISTANCE_THRESHOLD_KM

def test_same_point_distance_zero():
    dist = calculate_geodesic_distance(-33.036, -71.62963, -33.036, -71.62963)
    assert pytest.approx(dist, abs=1e-3) == 0.0

def test_valparaiso_to_santiago_distance():
    # Valparaíso (-33.036, -71.62963) a Santiago (-33.4489, -70.6693) son aprox ~100 km
    dist = calculate_geodesic_distance(-33.036, -71.62963, -33.4489, -70.6693)
    assert 90.0 < dist < 120.0
    assert dist < DISTANCE_THRESHOLD_KM

def test_sismo_valparaiso_coverage():
    # Epicentro cerca de costa de Valparaíso (-33.012, -71.745)
    epicenter_lat = -33.012
    epicenter_lon = -71.745

    valpo = SUBSCRIBER_CITIES["valparaiso"]
    coquimbo = SUBSCRIBER_CITIES["coquimbo"]
    concepcion = SUBSCRIBER_CITIES["concepcion"]
    arica = SUBSCRIBER_CITIES["arica"]
    punta_arenas = SUBSCRIBER_CITIES["punta_arenas"]

    d_valpo = calculate_geodesic_distance(valpo.lat, valpo.lon, epicenter_lat, epicenter_lon)
    d_coquimbo = calculate_geodesic_distance(coquimbo.lat, coquimbo.lon, epicenter_lat, epicenter_lon)
    d_concepcion = calculate_geodesic_distance(concepcion.lat, concepcion.lon, epicenter_lat, epicenter_lon)
    d_arica = calculate_geodesic_distance(arica.lat, arica.lon, epicenter_lat, epicenter_lon)
    d_punta_arenas = calculate_geodesic_distance(punta_arenas.lat, punta_arenas.lon, epicenter_lat, epicenter_lon)

    # Valparaíso debe estar muy cerca (< 50 km)
    assert d_valpo < DISTANCE_THRESHOLD_KM
    # Coquimbo está a aprox 340 km (< 500 km)
    assert d_coquimbo < DISTANCE_THRESHOLD_KM
    # Concepción está a aprox 440 km (< 500 km)
    assert d_concepcion < DISTANCE_THRESHOLD_KM
    # Arica y Punta Arenas están a más de 1500 km (> 500 km)
    assert d_arica > DISTANCE_THRESHOLD_KM
    assert d_punta_arenas > DISTANCE_THRESHOLD_KM

def test_sismo_arica_coverage():
    # Epicentro en Arica (-18.650, -70.420)
    epicenter_lat = -18.650
    epicenter_lon = -70.420

    d_arica = calculate_geodesic_distance(
        SUBSCRIBER_CITIES["arica"].lat,
        SUBSCRIBER_CITIES["arica"].lon,
        epicenter_lat,
        epicenter_lon
    )
    d_valpo = calculate_geodesic_distance(
        SUBSCRIBER_CITIES["valparaiso"].lat,
        SUBSCRIBER_CITIES["valparaiso"].lon,
        epicenter_lat,
        epicenter_lon
    )

    assert d_arica < DISTANCE_THRESHOLD_KM
    assert d_valpo > DISTANCE_THRESHOLD_KM
