# Tarea 1 - INF326 "Arquitectura de Software"
## Sistema de Notificación de Sismos (Publish-Subscribe + Pull HTTP)

Departamento de Informática  
Universidad Técnica Federico Santa María  

---

## 1. Integrantes y Roles

| Nombre | Rol USM | 
|---|---|
| *Benjamín López* | *202273081-1* |
| *Marco Repetto* | *202103059-k* | 


## 2. Descripción General de la Arquitectura

El sistema implementa el patrón arquitectónico **Publish-Subscribe** complementado con una adaptación del **modelo Pull** para la consulta de información sísmica detallada:

1. **Broker de Mensajería (CloudAMQP / RabbitMQ):**
   - Utiliza un Exchange de tipo `fanout` (`sismos_events`).
   - El componente **Publisher** notifica la ocurrencia de sismos emitiendo eventos con **mínima información** (`id`, `latitud`, `longitud`, `timestamp`).
2. **5 Componentes Suscriptores:**
   - Ubicados geográficamente en: **Arica**, **Coquimbo**, **Valparaíso**, **Concepción** y **Punta Arenas**.
   - Cada suscriptor cuenta con una cola durable exclusiva vinculada al exchange.
   - Al recibir un evento sísmico, calcula la distancia geodésica mediante la **fórmula de Haversine**.
   - **Criterio de Interés:** Si la distancia es **menor a 500 [km]**, el suscriptor ejecuta una petición HTTP `GET /sismos/{id}` al servicio FastAPI para obtener la ficha técnica completa; de lo contrario, descarta el evento.
3. **Servicio HTTP de Datos de Sismos (FastAPI):**
   - Expone endpoints REST para consultar la información detallada basada en la estructura real de [sismologia.cl](https://sismologia.cl) (Fecha UTC/Local, Profundidad, Magnitud, Escala, Referencia geográfica).

---

## 3. Estructura del Repositorio

```plaintext
INF326-tarea-1-publisher-subscribe/
├── README.md                     # Documentación principal e instrucciones
├── TRADE_OFFS_Y_BOTE.md          # Discusión de Trade-offs y Back of the Envelope
├── requirements.txt              # Dependencias del proyecto
├── pytest.ini                    # Configuración de pruebas automatizadas
├── .env.example                  # Plantilla de variables de entorno (CloudAMQP / URLs)
├── .env                          # Configuración local de entorno
│
├── config/                       # Módulo de configuración
│   ├── __init__.py
│   └── settings.py               # Lectura de variables de entorno (.env)
│
├── common/                       # Módulos comunes y compartidos
│   ├── __init__.py
│   ├── distance.py               # Cálculo de distancia geodésica (Haversine)
│   ├── models.py                 # Esquemas de datos (Pydantic)
│   └── subscribers_config.py    # Coordenadas oficiales de las 5 ciudades
│
├── api/                          # Servicio HTTP de Datos (FastAPI)
│   ├── __init__.py
│   ├── main.py                   # API REST y endpoints
│   └── mock_data.py              # Catálogo en memoria con sismos chilenos
│
├── publisher/                    # Componente Publicador de Sismos
│   ├── __init__.py
│   └── publisher.py              # CLI para emitir eventos sísmicos mínimos
│
├── subscriber/                   # Componentes Suscriptores
│   ├── __init__.py
│   └── subscriber.py             # Lógica base de un suscriptor geolocalizado
│
└── tests/                        # Pruebas automatizadas (pytest)
    ├── test_distance.py          # Pruebas del cálculo de distancia y umbral 500 km
    ├── test_api.py               # Pruebas de endpoints FastAPI
    └── test_messages.py          # Pruebas de validación de esquemas de mensajes
```

---

## 4. Pre-requisitos e Instalación

### 4.1. Requisitos
- **Python 3.10** o superior.
- **Acceso a un Broker AMQP**

### 4.2. Instalación de Dependencias
```bash
# Crear y activar entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4.3. Configuración de Variables de Entorno (`.env`)
Crear o editar el archivo `.env` en la raíz del proyecto (basado en `.env.example`):
```ini
# Si utilizas CloudAMQP, copia aquí tu URL de conexión:
CLOUDAMQP_URL=amqps://usuario:password@host.cloudamqp.com/vhost

# O si utilizas RabbitMQ local:
# CLOUDAMQP_URL=amqp://guest:guest@localhost:5672/

EXCHANGE_NAME=sismos_events
HTTP_SERVICE_URL=http://localhost:8000
```

---

## 5. Instrucciones de Ejecución

Para probar el flujo completo se requieren **3 terminales** (o ejecutar los suscriptores en conjunto):

### Terminal 1: Iniciar el Servicio HTTP (FastAPI)
```bash
uvicorn api.main:app --reload --port 8000
```
*El servicio estará disponible en `http://localhost:8000`. La documentación Swagger interactiva puede verse en `http://localhost:8000/docs`.*

---

### Terminal 2: Iniciar los Suscriptores

#### Opción A: Abrir 5 ventanas de terminal independientes automáticamente
```bash
./scripts/start_subscribers.sh
```
*Detecta automáticamente tu emulador de terminal (`ptyxis`, `alacritty`, `kitty`, `gnome-terminal`, `tmux`) y abre 5 consolas separadas, una para cada ciudad.*

#### Opción B: Iniciar suscriptores de forma individual manualmente
```bash
python -m subscriber.subscriber --city valparaiso
python -m subscriber.subscriber --city coquimbo
python -m subscriber.subscriber --city arica
python -m subscriber.subscriber --city concepcion
python -m subscriber.subscriber --city punta_arenas
```

---

### Terminal 3: Publicar Eventos Sísmicos (Publisher)

#### Opción Interactiva:
```bash
python publisher/publisher.py
```
*Muestra un menú para seleccionar el sismo a emitir.*

#### Opción por Preset (CLI):
```bash
# Sismo en la costa de Valparaíso (Activa Valparaíso, Coquimbo y Concepción)
python publisher/publisher.py --preset sismo-valparaiso-01

# Sismo en el extremo norte (Activa únicamente Arica)
python publisher/publisher.py --preset sismo-arica-01

# Sismo en Magallanes (Activa únicamente Punta Arenas)
python publisher/publisher.py --preset sismo-punta-arenas-01
```

---

## 6. Ejecución de Pruebas Automatizadas

El proyecto incluye una suite de pruebas con `pytest` que valida el cálculo de distancia geodésica, el umbral de 500 km, la API REST y el diseño de mensajes:

```bash
pytest tests/ -v
```

---

## 7. Discusión de Trade-offs y "Back of the Envelope"

La discusión requerida por la pauta de evaluación acerca de los *Trade-offs* de la arquitectura y la estimación de *Back of the Envelope* se encuentra detallada en el archivo:
```plaintext
TRADE_OFFS_Y_BOTE.md
```