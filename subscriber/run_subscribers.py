import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import threading
import time
import datetime
from common.subscribers_config import SUBSCRIBER_CITIES
from subscriber.subscriber import EarthquakeSubscriber

def log(level: str, msg: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [{level.upper()}] [ORCHESTRATOR] {msg}")

def run_subscriber_thread(city_key: str):
    try:
        sub = EarthquakeSubscriber(city_key=city_key)
        sub.start()
    except Exception as e:
        log("ERROR", f"Fallo en ejecucion de suscriptor {city_key}: {e}")

def main():
    log("INFO", "Iniciando orquestador de suscriptores (5 ciudades)")
    log("INFO", f"Nodos configurados: {', '.join(SUBSCRIBER_CITIES.keys())}")

    threads = []
    for city_key in SUBSCRIBER_CITIES.keys():
        t = threading.Thread(target=run_subscriber_thread, args=(city_key,), daemon=True)
        t.start()
        threads.append(t)
        time.sleep(0.2)

    log("INFO", "Todos los suscriptores han sido iniciados correctamente. Presione Ctrl+C para detener.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("INFO", "Deteniendo orquestador y cerrando suscriptores.")
        sys.exit(0)

if __name__ == "__main__":
    main()
