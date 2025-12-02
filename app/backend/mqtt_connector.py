import logging
import sys
import requests
from app.backend import MAIoTALib

API_BASE_URL = "http://localhost:8000/api"
SENSOR_MAPPING: dict[str, int] = {}
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [MQTT_EXT] - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def discover_sensors():
    """
    Fetches existing sensors from the API and maps them to MAIoTA data types.
    """
    global SENSOR_MAPPING
    try:
        logger.info("Discovering sensors from Agrotech API...")
        resp = requests.get(f"{API_BASE_URL}/parcels")
        if resp.status_code != 200:
            logger.error("Failed to fetch parcels from API.")
            return
        parcels = resp.json()
        if not parcels:
            logger.warning("No parcels found in Agrotech system.")
            return
        target_parcel = next(
            (p for p in parcels if "Greenhouse" in p["name"]), parcels[0]
        )
        logger.info(
            f"Targeting Parcel: {target_parcel['name']} (ID: {target_parcel['id']})"
        )
        resp = requests.get(f"{API_BASE_URL}/parcels/{target_parcel['id']}/sensors")
        if resp.status_code == 200:
            sensors = resp.json()
            for sensor in sensors:
                s_type = sensor["type"]
                s_id = sensor["id"]
                if s_type in [
                    "temperature",
                    "humidity",
                    "soil_moisture",
                    "light",
                    "co2",
                    "cov",
                    "nox",
                ]:
                    SENSOR_MAPPING[s_type] = s_id
                    logger.info(f"Mapped '{s_type}' -> Sensor ID {s_id}")
        else:
            logger.error(f"Failed to fetch sensors for parcel {target_parcel['id']}")
        if not SENSOR_MAPPING:
            logger.warning(
                "No compatible sensors found in the target parcel. Data will not be saved."
            )
    except Exception as e:
        logger.exception(f"Discovery failed: {e}")


def parse_maiota_payload(payload: str) -> dict[str, float]:
    """
    Parses the specific format:
    Payload=CIoTA-D1=2603&D2=5411&D3=2542&D4=43&D5=580&D6=103&D7=1&
    """
    results = {}
    try:
        if "Payload=" in payload:
            payload = payload.split("Payload=")[1]
        clean_payload = payload.strip().rstrip("&")
        parts = clean_payload.split("&")
        raw_values = {}
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                clean_val_str = value.replace("↓", "").replace("%", "").strip()
                try:
                    raw_values[key] = float(clean_val_str)
                except ValueError:
                    logger.exception(f"Could not parse value '{value}' for key '{key}'")
                    continue
        for key, val in raw_values.items():
            k = key.split("-")[-1].strip() if "-" in key else key.strip()
            if k == "D1":
                results["temperature"] = val / 100.0
            elif k == "D2":
                results["humidity"] = val / 100.0
            elif k == "D3":
                results["soil_moisture"] = val / 100.0
            elif k == "D4":
                results["light"] = val / 10.0
            elif k == "D5":
                results["co2"] = val
            elif k == "D6":
                results["cov"] = val
            elif k == "D7":
                results["nox"] = val
        return results
    except Exception as e:
        logger.exception(f"Failed to parse payload '{payload}': {e}")
        return {}


def post_reading(sensor_id: int, value: float, source_type: str):
    """Sends the processed reading to the Agrotech API."""
    url = f"{API_BASE_URL}/sensors/{sensor_id}/data"
    payload = {
        "value": value,
        "raw": f"MAIoTA_{source_type.upper()}",
        "timestamp": None,
    }
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            logger.info(f"SAVED [ID={sensor_id} {source_type.upper()}]: {value}")
        else:
            logger.warning(
                f"API ERROR [ID={sensor_id}]: {resp.status_code} - {resp.text}"
            )
    except requests.exceptions.RequestException as e:
        logger.exception(f"Connection error posting to API: {e}")


def dispatch_data(data: dict[str, float]):
    """Distributes parsed data to mapped sensors."""
    for data_type, value in data.items():
        if data_type in SENSOR_MAPPING:
            sensor_id = SENSOR_MAPPING[data_type]
            post_reading(sensor_id, value, data_type)
        else:
            pass


original_on_connect = MAIoTALib.client.on_connect
original_on_message = MAIoTALib.client.on_message


def extended_on_connect(client, userdata, flags, rc):
    if original_on_connect:
        original_on_connect(client, userdata, flags, rc)
    if rc == 0:
        logger.info("Agrotech Extension: Connected to Broker. Ready to process data.")


def extended_on_message(client, userdata, msg):
    if original_on_message:
        original_on_message(client, userdata, msg)
    try:
        payload_str = str(msg.payload.decode("utf-8"))
        parsed_data = parse_maiota_payload(payload_str)
        if parsed_data:
            dispatch_data(parsed_data)
    except Exception as e:
        logger.exception(f"Error in extended message processing: {e}")


if __name__ == "__main__":
    print("Initializing Agrotech MQTT Integration...")
    discover_sensors()
    MAIoTALib.client.on_connect = extended_on_connect
    MAIoTALib.client.on_message = extended_on_message
    import paho.mqtt.client as mqtt

    _original_loop_forever = mqtt.Client.loop_forever

    def mock_loop_forever(
        self, timeout=1.0, max_packets=1, retry_first_connection=False
    ):
        print("Agrotech: Intercepted loop_forever to inject extensions...")
        return

    mqtt.Client.loop_forever = mock_loop_forever
    from app.backend import MAIoTALib

    mqtt.Client.loop_forever = _original_loop_forever
    print("Agrotech: Injecting extended callbacks...")
    discover_sensors()
    MAIoTALib.client.on_connect = extended_on_connect
    MAIoTALib.client.on_message = extended_on_message
    print("Agrotech: Starting Main Loop...")
    MAIoTALib.client.loop_forever()