import time
import random
import requests
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [SIMULATOR] - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)
API_BASE_URL = "http://localhost:8000/api"
SIMULATION_INTERVAL = 5
PARCELS_ENDPOINT = f"{API_BASE_URL}/parcels"


def get_sensor_url(sensor_id: int) -> str:
    return f"{API_BASE_URL}/sensors/{sensor_id}/data"


def get_sensors_url(parcel_id: int) -> str:
    return f"{API_BASE_URL}/parcels/{parcel_id}/sensors"


class SensorSimulator:
    def __init__(self):
        self.active_sensors: list[dict] = []

    def fetch_configuration(self):
        """
        Fetches the current list of parcels and sensors from the API
        to configure the simulator with valid IDs.
        """
        try:
            logger.info("Fetching system configuration...")
            resp = requests.get(PARCELS_ENDPOINT)
            if resp.status_code != 200:
                logger.error(f"Failed to fetch parcels. Status: {resp.status_code}")
                return
            parcels = resp.json()
            logger.info(f"Found {len(parcels)} parcels.")
            self.active_sensors = []
            for parcel in parcels:
                p_id = parcel["id"]
                resp = requests.get(get_sensors_url(p_id))
                if resp.status_code == 200:
                    sensors = resp.json()
                    for s in sensors:
                        self.active_sensors.append(s)
                        logger.info(
                            f"Configured sensor: ID={s['id']} Type={s['type']} ({parcel['name']})"
                        )
                else:
                    logger.warning(f"Failed to fetch sensors for parcel {p_id}")
            logger.info(
                f"Simulation configured with {len(self.active_sensors)} active sensors."
            )
        except requests.exceptions.ConnectionError as e:
            logger.exception(
                f"Could not connect to API. Is the Agrotech server running at http://localhost:8000? Error: {e}"
            )
            sys.exit(1)
        except Exception as e:
            logger.exception(f"Configuration failed: {e}")
            sys.exit(1)

    def generate_value(self, sensor_type: str, last_val: float = None) -> float:
        """
        Generates a realistic value based on sensor type and random drift.
        """
        base_values = {
            "temperature": 24.0,
            "humidity": 55.0,
            "soil_moisture": 35.0,
            "light": 800.0,
            "other": 50.0,
        }
        current = (
            last_val if last_val is not None else base_values.get(sensor_type, 50.0)
        )
        if sensor_type == "temperature":
            change = random.uniform(-0.5, 0.5)
            new_val = current + change
            new_val = max(10.0, min(45.0, new_val))
        elif sensor_type == "humidity":
            change = random.uniform(-2.0, 2.0)
            new_val = max(0.0, min(100.0, current + change))
        elif sensor_type == "soil_moisture":
            change = random.uniform(-1.0, 1.0)
            new_val = max(0.0, min(100.0, current + change))
        elif sensor_type == "light":
            change = random.uniform(-50, 50)
            new_val = max(0.0, min(2000.0, current + change))
        else:
            new_val = current + random.uniform(-1, 1)
        if random.random() < 0.05:
            if sensor_type == "temperature":
                new_val += 15
            elif sensor_type == "soil_moisture":
                new_val -= 25
        return round(new_val, 2)

    def run(self):
        """Main simulation loop."""
        self.fetch_configuration()
        if not self.active_sensors:
            logger.warning("No sensors found to simulate. Exiting.")
            return
        last_values = {}
        logger.info(
            f"Starting simulation loop (Interval: {SIMULATION_INTERVAL}s)... Press Ctrl+C to stop."
        )
        try:
            while True:
                for sensor in self.active_sensors:
                    s_id = sensor["id"]
                    s_type = sensor["type"]
                    val = self.generate_value(s_type, last_values.get(s_id))
                    last_values[s_id] = val
                    payload = {"value": val, "raw": f"SIM_{int(time.time())}"}
                    try:
                        resp = requests.post(get_sensor_url(s_id), json=payload)
                        if resp.status_code == 200:
                            logger.info(
                                f"SENT [Sensor {s_id} | {s_type}]: {val} {sensor.get('unit', '')}"
                            )
                        else:
                            logger.warning(
                                f"FAILED [Sensor {s_id}]: API returned {resp.status_code}"
                            )
                    except Exception as e:
                        logger.exception(f"ERROR sending to Sensor {s_id}: {e}")
                time.sleep(SIMULATION_INTERVAL)
        except KeyboardInterrupt as e:
            logger.exception(f"Simulation stopped by user: {e}")


if __name__ == "__main__":
    sim = SensorSimulator()
    sim.run()