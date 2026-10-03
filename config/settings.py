import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Settings:
    AMQP_URL: str = os.getenv("CLOUDAMQP_URL") or os.getenv("AMQP_URL") or "amqp://guest:guest@localhost:5672/"
    EXCHANGE_NAME: str = os.getenv("EXCHANGE_NAME", "sismos_events")
    HTTP_SERVICE_URL: str = os.getenv("HTTP_SERVICE_URL", "http://localhost:8000")
    DISTANCE_THRESHOLD_KM: float = float(os.getenv("DISTANCE_THRESHOLD_KM", "500.0"))

settings = Settings()
