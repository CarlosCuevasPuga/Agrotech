# Sistema de Monitorización Agrícola (Agrotech)

![Agrotech Banner](/placeholder.svg)

**Agrotech** es una plataforma integral *full-stack* desarrollada en Python con **Reflex**, diseñada para la monitorización en tiempo real de cultivos agrícolas mediante sensores IoT. El sistema integra una arquitectura completa de ingesta de datos, procesamiento, almacenamiento y visualización.

## 🚀 Características Principales

| Característica | Descripción |
|----------------|-------------|
| **Dashboard en Tiempo Real** | Monitorización visual con actualización automática (cada 30s) y sparklines históricos. |
| **Integración IoT (MQTT)** | **Conector real** compatible con sensores MAIoTA y la librería `MAIoTALib`. |
| **Gestión de Parcelas** | CRUD completo para organizar sensores por zonas geográficas. |
| **Sistema de Alertas** | Detección automática de umbrales críticos con notificaciones visuales. |
| **Analítica Histórica** | Gráficos detallados con filtros de fecha para analizar tendencias. |
| **API RESTful** | Interfaz programática completa (FastAPI) para la gestión externa. |
| **Seguridad** | Autenticación robusta basada en roles (Admin/Técnico) y cifrado PBKDF2. |

## 📡 Integración MQTT Real con Código Original

Este proyecto destaca por su **integración no invasiva** con el código proporcionado para el Reto Agrotech.

### 1. Código Original Intacto
El archivo `app/backend/MAIoTALib.py` contiene el código fuente **original y sin modificaciones**:
- **Nombre**: `MAIoTALib.py`
- **Versión**: 1.0 (26/10/2025)
- **Autor**: ©Antonio Hurtado

Esto garantiza compatibilidad total con las especificaciones del sensor MAIoTA. El código original soporta dos versiones del cliente Paho MQTT (Versión 1 y Versión 2), estando configurado por defecto para la **Versión 1**.

### 2. Arquitectura de Extensión
En lugar de modificar el código base, hemos creado `app/backend/mqtt_connector.py`, un módulo que importa la librería original y extiende sus capacidades para permitir:
- Persistencia de datos en SQLite.
- Visualización en tiempo real en Web.
- Sistema de alertas.

### 3. Tabla de Especificaciones MAIoTA (Según Código Original)

| Dato | Descripción | Operación / Notas |
|------|-------------|-------------------|
| **D1** | Temperatura Ambiente | Se divide entre 100. Valor en ºC |
| **D2** | Humedad Ambiente | Se divide entre 100. Valor en % |
| **D3** | Humedad Suelo | Se divide entre 100. Valor en %. *Nota: Si es < 24.65 aparece una flecha ↓* |
| **D4** | Iluminación | Se divide entre 10. Valor en Lux |
| **D5** | CO2 | No se opera. Valor en ppm |
| **D6** | COV | No se opera. Valor en Index |
| **D7** | NOx | No se opera. Valor en Index |

### 📝 Ejemplo de Procesamiento Real

**Payload Recibido (Crudo):**
text
Payload=CIoTA-D1=2603&D2=5411&D3=2542&D4=43&D5=580&D6=103&D7=1&


**Transformación y Almacenamiento:**
1. **D1 (Temp)**: `2603` → `26.03` → Guardado en sensor tipo `temperature`
2. **D2 (Hum)**: `5411` → `54.11` → Guardado en sensor tipo `humidity`
3. **D3 (Suelo)**: `2542` → `25.42` → Guardado en sensor tipo `soil_moisture`
4. **D4 (Luz)**: `43` → `4.3` → Guardado en sensor tipo `light`

> 📘 **Nota Técnica**: El sistema maneja automáticamente casos especiales como el símbolo de flecha baja (`↓`) en la humedad del suelo, limpiando el valor antes de procesarlo.

## 🛠️ Guía de Instalación y Ejecución

### 1. Preparar el Entorno
bash
# Clonar repositorio
git clone https://github.com/tu-usuario/agrotech.git
cd agrotech

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# Instalar dependencias (incluye reflex, fastapi, paho-mqtt)
pip install -r requirements.txt


### 2. Inicializar Base de Datos
Ejecuta el script de "seed" para crear usuarios, parcelas y sensores por defecto.
bash
python -m app.backend.seed_data


### 3. Ejecutar la Aplicación Web (Terminal 1)
bash
reflex run

Accede al dashboard en: `http://localhost:3000`

### 4. Instalación Específica MQTT (Sensor MAIoTA)

Para el funcionamiento correcto de la librería original `MAIoTALib.py`, es necesario instalar `paho-mqtt` siguiendo estas instrucciones exactas:

**Linux:**
bash
sudo apt install python3-paho-mqtt


**Windows:**
bash
pip install paho-mqtt
python.exe -m pip install --upgrade pip


### 5. Iniciar Conector MQTT (Terminal 2)
Para recibir datos en tiempo real del sensor MAIoTA:
bash
python -m app.backend.mqtt_connector

Verás logs como: `[MQTT] - INFO - SENT [ID=1 TEMPERATURE]: 26.03`

## 🔑 Credenciales de Acceso

| Rol | Usuario | Contraseña | Acceso |
|-----|---------|------------|--------|
| **Administrador** | `admin` | `admin123` | Control total del sistema |
| **Técnico** | `tech_user` | `securePass!` | Visualización y gestión operativa |

## 📂 Estructura del Proyecto

text
agrotech/
├── app/
│   ├── api/            # Endpoints FastAPI (Ingesta de datos)
│   ├── backend/        # Lógica de negocio, DB y MQTT Connector
│   │   ├── database.py       # Gestor de SQLite
│   │   ├── mqtt_connector.py # Servicio de conexión IoT
│   │   └── MAIoTALib.py      # Lógica de parsing original
│   ├── components/     # Componentes UI reutilizables (Reflex)
│   ├── pages/          # Páginas (Dashboard, Analytics, etc.)
│   ├── states/         # Gestión del estado reactivo
│   └── app.py          # Punto de entrada Reflex
├── assets/             # Recursos estáticos
└── agrotech_data.db    # Base de datos SQLite (autogenerada)


## 📚 Documentación Adicional
- [Guía de Inicio Rápido (QUICKSTART)](app/QUICKSTART.md)
- [Arquitectura del Sistema](app/ARCHITECTURE.md)
- [Guía de Contribución](app/CONTRIBUTING.md)

## 🏅 Reconocimientos

Este proyecto utiliza la librería de conexión **MAIoTALib** para la integración con sensores IoT.
- **Autor Original**: Antonio Hurtado
- **Versión**: 1.0 (26/10/2025)
- **Contexto**: Reto Agrotech

Agradecemos al autor por proporcionar el código base que hace posible la comunicación MQTT con los dispositivos MAIoTA.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

--- 
Desarrollado con ❤️ usando [Reflex](https://reflex.dev/).
