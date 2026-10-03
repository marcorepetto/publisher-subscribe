import math

EARTH_RADIUS_KM = 6371.0

def calculate_geodesic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia geodésica entre dos puntos en la superficie terrestre
    utilizando la fórmula del semiverseno (Haversine).

    :param lat1: Latitud del punto 1 en grados decimales
    :param lon1: Longitud del punto 1 en grados decimales
    :param lat2: Latitud del punto 2 en grados decimales
    :param lon2: Longitud del punto 2 en grados decimales
    :return: Distancia en kilómetros (km)
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)

    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c
