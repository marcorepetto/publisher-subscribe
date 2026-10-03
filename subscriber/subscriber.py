import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import json
import argparse
import datetime
import httpx
import pika
from config.settings import settings
from common.models import MinimalEarthquakeEvent, EarthquakeDetail
from common.distance import calculate_geodesic_distance
from common.subscribers_config import SUBSCRIBER_CITIES, DISTANCE_THRESHOLD_KM, SubscriberLocation

class EarthquakeSubscriber:
    """
    Componente suscriptor geolocalizado en una ciudad.
    Recibe notificaciones de sismos con datos mínimos mediante AMQP (Exchange fanout),
    determina si el evento está dentro de su radio de interés (500 km) y, en caso afirmativo,
    hace pull de la información completa desde el servicio HTTP.
    """
    def __init__(self, city_key: str, location: SubscriberLocation = None, http_url: str = None, amqp_url: str = None):
        self.city_key = city_key.lower()
        if location:
            self.location = location
        elif self.city_key in SUBSCRIBER_CITIES:
            self.location = SUBSCRIBER_CITIES[self.city_key]
        else:
            raise ValueError(f"Ciudad desconocida: {city_key}. Opciones válidas: {list(SUBSCRIBER_CITIES.keys())}")
        
        self.http_url = http_url or settings.HTTP_SERVICE_URL
        self.amqp_url = amqp_url or settings.AMQP_URL
        self.exchange_name = settings.EXCHANGE_NAME
        self.threshold_km = settings.DISTANCE_THRESHOLD_KM

    def _log(self, level: str, message: str):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] [{level.upper()}] [{self.location.name}] {message}")

    def _fetch_detailed_info(self, sismo_id: str):
        """Realiza el llamado HTTP GET al servicio de datos de sismos."""
        url = f"{self.http_url.rstrip('/')}/sismos/{sismo_id}"
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    detail = EarthquakeDetail(**data)
                    return detail
                else:
                    self._log("ERROR", f"HTTP {response.status_code} al consultar endpoint {url}")
                    return None
        except Exception as e:
            self._log("ERROR", f"Excepcion de conexion con servicio HTTP ({url}): {e}")
            return None

    def process_message(self, ch, method, properties, body):
        try:
            payload = json.loads(body.decode("utf-8"))
            event = MinimalEarthquakeEvent(**payload)

            distance = calculate_geodesic_distance(
                self.location.lat,
                self.location.lon,
                event.latitud,
                event.longitud
            )

            self._log("INFO", f"Evento recibido | ID: {event.id} | Epicentro: ({event.latitud}, {event.longitud}) | Distancia: {distance:.2f} km | Umbral: {self.threshold_km:.0f} km")

            if distance <= self.threshold_km:
                self._log("INFO", f"CRITERIO CUMPLIDO: Distancia {distance:.2f} km <= {self.threshold_km:.0f} km. Ejecutando Pull HTTP...")
                
                detail = self._fetch_detailed_info(event.id)
                if detail:
                    self._log("INFO", f"DETALLE SISMO RECIBIDO | ID: {detail.id} | Magnitud: {detail.magnitud} {detail.escala} | Profundidad: {detail.profundidad_km} km | Fecha UTC: {detail.fecha_utc} | Ref: {detail.referencia_geografica}")
                else:
                    self._log("WARN", f"No fue posible recuperar la ficha detallada del sismo ID '{event.id}'.")
            else:
                self._log("INFO", f"DESCARTADO: Distancia {distance:.2f} km > {self.threshold_km:.0f} km. Fuera de radio de cobertura.")

        except Exception as e:
            self._log("ERROR", f"Fallo al procesar mensaje AMQP: {e}")

    def start(self):
        """Conecta al broker y comienza a escuchar eventos en su cola exclusiva."""
        masked_url = self.amqp_url.split('@')[-1] if '@' in self.amqp_url else self.amqp_url
        self._log("INFO", f"Conectando a broker AMQP: {masked_url}...")
        
        params = pika.URLParameters(self.amqp_url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # Declarar exchange fanout
        channel.exchange_declare(exchange=self.exchange_name, exchange_type="fanout", durable=True)

        # Cola exclusiva y temporal para este suscriptor
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        # Vincular cola al exchange
        channel.queue_bind(exchange=self.exchange_name, queue=queue_name)

        self._log("INFO", f"Suscriptor activo en cola '{queue_name}' | Coordenadas: ({self.location.lat}, {self.location.lon}) | Esperando eventos...")

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.process_message,
            auto_ack=True
        )

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            self._log("INFO", "Cerrando conexion de suscriptor...")
            channel.stop_consuming()
            connection.close()

def main():
    parser = argparse.ArgumentParser(description="Suscriptor de Notificaciones Sismicas (INF-326)")
    parser.add_argument(
        "--city",
        type=str,
        required=True,
        choices=list(SUBSCRIBER_CITIES.keys()),
        help=f"Ciudad del suscriptor: {list(SUBSCRIBER_CITIES.keys())}"
    )
    args = parser.parse_args()

    subscriber = EarthquakeSubscriber(city_key=args.city)
    subscriber.start()

if __name__ == "__main__":
    main()
