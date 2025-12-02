# 🚀 Agrotech - Guía de Inicio Rápido

Bienvenido al sistema de monitorización agrícola Agrotech.

## 1. Configuración Inicial

Antes de empezar, asegúrate de instalar las dependencias necesarias.

**Instalación General (App Web):**
bash
pip install -r requirements.txt


**Instalación Específica MQTT (Sensor MAIoTA):**
Siguiendo estrictamente las instrucciones incluidas en el archivo original `MAIoTALib.py` (©Antonio Hurtado, v1.0):

**Para Linux:**
Ejecuta el siguiente comando o uno similar dependiendo de la distro:
bash
sudo apt install python3-paho-mqtt


**Para Windows:**
Ejecuta los siguientes comandos:
bash
pip install paho-mqtt
python.exe -m pip install --upgrade pip


## 2. Iniciar la Aplicación Web

En una terminal, inicia el servidor Reflex (Frontend + Backend API):

bash
reflex run


> Accede a: `http://localhost:3000`
> Credenciales: `admin` / `admin123`

---

## 3. Conectar el Sensor MAIoTA (MQTT)

El sistema integra el código original `MAIoTALib.py` (ver 1.0. 26/10/2025. ©Antonio Hurtado).

### Versiones del Código (Importante)
El código original soporta dos versiones de la librería Paho MQTT. El sistema Agrotech está configurado para usar la **Versión 1**.

**Configuración Actual (Versión 1):**
En el archivo `app/backend/MAIoTALib.py`, las líneas activas (descomentadas) corresponden a:
1.  **Cliente:** `client = mqtt.Client()` (Sin parámetros de versión)
2.  **Callback:** `def on_connect(client, userdata, flags, rc):`

*Nota: Las líneas correspondientes a la Versión 2 (CallbackAPIVersion.VERSION2) están comentadas por defecto.*

### Parámetros de Conexión
- **Broker**: `broker.emqx.io`
- **Puerto**: `1883`
- **Topic**: `Awi7LJfyyn6LPjg/15046220`
- **Client ID**: `Equipo 1`

### Selecciona tu Modo de Ejecución

#### MODO A: Ejecución Original (Solo Verificación)
Ejecuta el archivo original tal cual fue entregado. Ideal para verificar la conexión básica sin guardar datos.

**Comando:**
bash
python app/backend/MAIoTALib.py


**Resultado Esperado:**
text
Conectado al Sensor MAIoTA con éxito. Los Payloads recibidos son: 
Mensaje recibido -> Payload=CIoTA-D1=2550&D2=6000&...

*Nota: En este modo los datos NO se guardan en el dashboard.*

#### MODO B: Conector Agrotech (Producción)
Usa el conector extendido que envuelve la librería original para guardar datos en la base de datos y generar alertas.

**Comando:**
bash
python -m app.backend.mqtt_connector


**Resultado Esperado:**
text
[MQTT_EXT] - INFO - Mapped 'temperature' -> Sensor ID 1
[MQTT_EXT] - INFO - Connected to Broker. Ready to process data.
[MQTT_EXT] - INFO - SAVED [ID=1 TEMPERATURE]: 25.5

*Nota: Los datos aparecerán automáticamente en http://localhost:3000*

---

## 4. Flujo de Datos

mermaid
graph LR
    Sensor(MAIoTA Device) -->|MQTT| Broker(broker.emqx.io)
    
    subgraph "Agrotech System"
        Connector[mqtt_connector.py]
        Original[MAIoTALib.py v1.0]
        API[FastAPI /api]
        DB[(SQLite)]
        UI[Reflex Dashboard]
    end
    
    Broker -->|Subscribe| Original
    Original -.->|Imported by| Connector
    Connector -->|Parse & POST| API
    API -->|Insert| DB
    DB -->|Auto Refresh| UI


## 5. Ejemplo de Procesamiento

Si el sensor envía: `Payload=CIoTA-D1=2603&D2=5411...`

El sistema lo traduce así en el Dashboard:
- **Temperatura**: 26.03 °C
- **Humedad**: 54.11 %
