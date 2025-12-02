# Integración MQTT - Sensor MAIoTA (Reto Agrotech)

## 1. Especificación Original del Código Base

Esta integración se basa estrictamente en el código proporcionado por el autor original.

**Cabecera del Código Original:**
text
MAIoTALib. Librería conexión con sensor MAIoTA, para Reto Agrotech en Python 3.11.2
ver 1.0. 26/10/2025. ©Antonio Hurtado


El sistema Agrotech respeta la autoría y la lógica de negocio definida en este archivo sin modificar su contenido, utilizando un patrón de extensión (wrapper) para añadir funcionalidades sin alterar el núcleo.

## 2. Versiones del Cliente MQTT

El código original está preparado para soportar dos versiones de la librería `paho-mqtt`. El sistema Agrotech utiliza por defecto la **Versión 1**, tal como está configurado en el archivo entregado.

### Versión 1 (Activa por defecto)
- **Instancia**: `client = mqtt.Client()`
- **Callback**: `def on_connect(client, userdata, flags, rc):`

### Versión 2 (Comentada en el original)
- **Instancia**: `client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)`
- **Callback**: `def on_connect(client, userdata, flags, rc, properties):`

> **Nota**: Si se desea usar la Versión 2, se deben descomentar las líneas correspondientes en `MAIoTALib.py` manualmente. Agrotech está configurado para funcionar con la Versión 1.

## 3. Instrucciones de Instalación Oficiales

Para el correcto funcionamiento de la librería original, se deben seguir las instrucciones exactas proporcionadas en el archivo fuente `MAIoTALib.py`:

**Para Linux:**
Ejecuta el siguiente comando o uno similar dependiendo de la distro:
bash
sudo apt install python3-paho-mqtt


**Para Windows:**
Ejecuta los siguientes comandos:
bash
pip install paho-mqtt
python.exe -m pip install --upgrade pip


## 4. Especificaciones del Payload

La trama de datos (`Payload`) sigue una estructura estricta definida por el autor original. A continuación se muestra la tabla de especificaciones exacta extraída del código fuente.

**Ejemplo de Trama:**
`Payload=CIoTA-D1=2603&D2=5411&D3=2542&D4=43&D5=580&D6=103&D7=1&`

### Tabla de Datos

| Dato | Descripción (Código Original) | Operación | Unidad Final |
|------|-------------------------------|-----------|--------------|
| **D1** | Temperatura Ambiente | Se divide entre 100 | **ºC** |
| **D2** | Humedad Ambiente | Se divide entre 100 | **%** |
| **D3** | Humedad Suelo | Se divide entre 100 | **%** |
| **D4** | Iluminación | Se divide entre 10 | **Lux** |
| **D5** | CO2 | No se opera | **ppm** |
| **D6** | COV | No se opera | **Index** |
| **D7** | NOx | No se opera | **Index** |

### Notas sobre los campos (Originales)
- **CIoTA-**: Es el identificador de trama. En el reto Agrotech siempre será lo mismo.
- **Identificación**: Cada dato viene identificado con `Dx=` (donde x toma valores de 1 a 7).
- **Terminación**: Cada dato termina con un `&`, ya que el contenido es variable. Optimiza la longitud del Payload.

### ⚠️ Caso Especial: Humedad del Suelo (D3)
El código original especifica un comportamiento especial para la humedad del suelo:

> *"El valor mínimo de data Humedad Suelo es 24.65. Cuando la humedad es inferior a este valor aparece una flecha ↓24.65 %."*

**Ejemplo:** `D3=↓2465`

El sistema Agrotech detecta y maneja este carácter especial (`↓`) automáticamente, limpiando el valor antes de procesarlo para evitar errores de conversión.

## 5. Arquitectura de Extensión

Para mantener el archivo `MAIoTALib.py` intacto, Agrotech utiliza un enfoque de envoltura:

1. **Importación**: `mqtt_connector.py` importa `MAIoTALib`.
2. **Intercepción**: Se inyectan callbacks extendidos (`extended_on_message`) que se ejecutan **además** de los originales.
3. **Procesamiento**: Los datos se parsean y envían a la base de datos mientras la consola sigue mostrando los `print` originales.

---

**Agradecimientos:**
Este sistema ha sido construido sobre la sólida base proporcionada por **Antonio Hurtado** (©2025), cuyo código `MAIoTALib.py` ha sido fundamental para la integración exitosa con los sensores MAIoTA.
