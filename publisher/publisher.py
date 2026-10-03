import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import json
import argparse
import datetime
import pika
from config.settings import settings
from common.models import MinimalEarthquakeEvent
from api.mock_data import SAMPLE_EARTHQUAKES

def log(level: str, msg: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{level.upper()}] [PUBLISHER] {msg}")

def publish_event(event: MinimalEarthquakeEvent, amqp_url: str = None, exchange_name: str = None):
    """
    Publica un evento sísmico con información mínima en el exchange fanout de RabbitMQ / CloudAMQP.
    """
    url = amqp_url or settings.AMQP_URL
    exchange = exchange_name or settings.EXCHANGE_NAME

    masked_url = url.split('@')[-1] if '@' in url else url
    log("INFO", f"Conectando a broker AMQP: {masked_url}")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Declaración de exchange fanout
    channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)

    payload = event.model_dump_json()
    channel.basic_publish(
        exchange=exchange,
        routing_key="",
        body=payload,
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2  # Mensaje persistente
        )
    )

    log("INFO", f"Evento publicado en exchange '{exchange}' | Payload: {payload}")
    connection.close()

def main():
    parser = argparse.ArgumentParser(description="Publisher de Eventos Sismicos (INF-326)")
    parser.add_argument(
        "--preset",
        type=str,
        choices=list(SAMPLE_EARTHQUAKES.keys()),
        help="Publicar uno de los sismos preconfigurados del catalogo"
    )
    parser.add_argument("--id", type=str, help="ID unico del sismo")
    parser.add_argument("--lat", type=float, help="Latitud del epicentro")
    parser.add_argument("--lon", type=float, help="Longitud del epicentro")
    parser.add_argument("--list-presets", action="store_true", help="Listar presets disponibles")

    args = parser.parse_args()

    if args.list_presets:
        print("\n--- Presets de Sismos en Catalogo ---")
        for key, sismo in SAMPLE_EARTHQUAKES.items():
            print(f" - {key}: {sismo.referencia_geografica} (Lat: {sismo.latitud}, Lon: {sismo.longitud}, Mag: {sismo.magnitud})")
        print("-------------------------------------\n")
        return

    if args.preset:
        detail = SAMPLE_EARTHQUAKES[args.preset]
        event = MinimalEarthquakeEvent(
            id=detail.id,
            latitud=detail.latitud,
            longitud=detail.longitud,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )
    elif args.id and args.lat is not None and args.lon is not None:
        event = MinimalEarthquakeEvent(
            id=args.id,
            latitud=args.lat,
            longitud=args.lon,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )
    else:
        print("\n=== Publicador de Eventos Sismicos ===")
        print("Seleccione un evento a emitir:")
        print("1. Sismo Valparaiso (Lat: -33.012, Lon: -71.745)")
        print("2. Sismo Arica (Lat: -18.650, Lon: -70.420)")
        print("3. Sismo Coquimbo (Lat: -30.120, Lon: -71.450)")
        print("4. Sismo Concepcion (Lat: -36.750, Lon: -73.210)")
        print("5. Sismo Punta Arenas (Lat: -53.400, Lon: -71.100)")
        print("6. Sismo Antofagasta (Lat: -23.650, Lon: -70.400)")
        choice = input("Opcion [1-6] (default 1): ").strip()
        
        mapping = {
            "": "sismo-valparaiso-01",
            "1": "sismo-valparaiso-01",
            "2": "sismo-arica-01",
            "3": "sismo-coquimbo-01",
            "4": "sismo-concepcion-01",
            "5": "sismo-punta-arenas-01",
            "6": "sismo-antofagasta-01",
        }
        preset_key = mapping.get(choice, "sismo-valparaiso-01")
        detail = SAMPLE_EARTHQUAKES[preset_key]
        event = MinimalEarthquakeEvent(
            id=detail.id,
            latitud=detail.latitud,
            longitud=detail.longitud,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )

    publish_event(event)

if __name__ == "__main__":
    main()
