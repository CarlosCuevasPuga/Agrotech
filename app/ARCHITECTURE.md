# Arquitectura del Sistema Agrotech

## 1. Descripción General

Agrotech es una aplicación web full-stack construida enteramente en Python utilizando el framework **Reflex**. El sistema sigue una arquitectura monolítica modular que integra el frontend, el backend y una API RESTful en una sola base de código cohesiva.

El objetivo principal es la ingestión, procesamiento y visualización eficiente de datos provenientes de sensores IoT en un contexto agrícola.

## 2. Diagrama de Componentes

ascii
+-------------------+       +-------------------+
|   Cliente Web     |       |   Dispositivos    |
| (Browser / React) |       |   IoT / Sensores  |
+--------+----------+       +---------+---------+
         |                            |
         | WebSocket / HTTP           | HTTP POST (JSON)
         v                            v
+---------------------------------------------------+
|                 Servidor Agrotech                 |
|                                                   |
|  +--------------+      +-----------------------+  |
|  |  Frontend    |      |      API REST         |  |
|  |  (Reflex UI) |      |      (FastAPI)        |  |
|  +------+-------+      +-----------+-----------+  |
|         |                          |              |
|         v                          v              |
|  +--------------+      +-----------------------+  |
|  |    State     |<---->|   Database Manager    |  |
|  |  Management  |      |    (Repository)       |  |
|  +--------------+      +-----------+-----------+  |
|                                    |              |
+------------------------------------+--------------+
                                     |
                                     v
                          +-----------------------+
                          |   SQLite Database     |
                          |   (agrotech_data.db)  |
                          +-----------------------+


## 3. Diseño de Base de Datos (Schema)

El sistema utiliza SQLite por su simplicidad y portabilidad. El esquema relacional consta de las siguientes tablas principales:

### `users`
- Gestión de acceso y roles.
- Campos: `id`, `username`, `password_hash` (PBKDF2), `role`.

### `parcels` (Parcelas)
- Representa unidades geográficas o lógicas de cultivo.
- Campos: `id`, `name`, `location`.

### `sensors`
- Dispositivos físicos asociados a una parcela.
- Campos: `id`, `parcel_id` (FK), `type` (temp, humidity, etc.), `threshold_low`, `threshold_high`.

### `sensor_data`
- Series temporales de lecturas.
- Campos: `id`, `sensor_id` (FK), `value`, `timestamp`, `raw`.

### `alerts`
- Eventos generados automáticamente cuando se violan umbrales.
- Campos: `id`, `sensor_id` (FK), `type`, `message`, `acknowledged`.

## 4. Flujo de Datos

### Ingestión de Datos
1. Un sensor envía un `POST` a `/api/sensors/{id}/data`.
2. El endpoint valida la existencia del sensor.
3. Se compara el valor con los umbrales (`threshold_low`, `threshold_high`).
4. Si hay violación, se crea un registro en la tabla `alerts`.
5. El dato se persiste en `sensor_data`.

### Visualización (Dashboard)
1. El cliente web solicita el estado inicial.
2. `SensorsState` consulta `DatabaseManager` para obtener parcelas y últimas lecturas.
3. Se procesan los datos para enriquecerlos con colores de estado (verde, amarillo, rojo).
4. Los datos se envían al cliente vía WebSocket.
5. Un proceso en segundo plano (`tick`) actualiza los datos cada 30 segundos.

## 5. Patrones de Diseño

- **Repository Pattern**: Toda la lógica de acceso a datos está encapsulada en la clase `DatabaseManager`, desacoplando los estados de Reflex de las consultas SQL directas.
- **State Management**: Uso de clases `rx.State` divididas por dominio (`AuthState`, `ParcelsState`, `SensorsState`) para mantener la lógica de negocio organizada.
- **Dependency Injection**: FastAPI inyecta dependencias en los endpoints de la API.

## 6. Seguridad

- **Hashing de Contraseñas**: Se utiliza PBKDF2-HMAC-SHA256 con salt aleatorio por usuario para almacenar credenciales.
- **Protección de Rutas**: Middleware en `AuthState.on_mount` verifica la sesión del usuario antes de renderizar páginas protegidas.
- **Validación de Datos**: Pydantic se utiliza en la capa de API para asegurar la integridad de los datos entrantes.
