import random
import logging
from datetime import datetime, timedelta
from app.backend.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_agrotech_db():
    """
    Initializes the Agrotech database with sample data:
    - Users (admin, technical)
    - Parcels (North Field, Greenhouse A, Orchard)
    - Sensors (Soil Moisture, Temp, Humidity, Light)
    - Historical Data (Last 24-48 hours)
    - Sample Alerts
    """
    logger.info("Starting Agrotech database seeding...")
    DatabaseManager.initialize_schema()
    if not DatabaseManager.get_user_by_username("admin"):
        DatabaseManager.create_user("admin", "admin123", role="admin")
        logger.info("Created user: admin")
    if not DatabaseManager.get_user_by_username("tech_user"):
        DatabaseManager.create_user("tech_user", "securePass!", role="technical")
        logger.info("Created user: tech_user")
    parcels_data = [
        {"name": "North Field (Corn)", "location": "Sector N-12"},
        {"name": "Greenhouse Alpha", "location": "Sector G-01"},
        {"name": "South Orchard", "location": "Sector S-05"},
    ]
    existing_parcels = DatabaseManager.get_parcels()
    if not existing_parcels:
        parcel_ids = []
        for p in parcels_data:
            pid = DatabaseManager.create_parcel(p["name"], p["location"])
            parcel_ids.append(pid)
            logger.info(f"Created parcel: {p['name']}")
    else:
        parcel_ids = [p["id"] for p in existing_parcels]
        logger.info("Parcels already exist, using existing IDs.")
    sensor_templates = [
        {
            "type": "temperature",
            "unit": "°C",
            "desc": "Ambient Air Temp (D1)",
            "low": 10.0,
            "high": 35.0,
        },
        {
            "type": "humidity",
            "unit": "%",
            "desc": "Relative Humidity (D2)",
            "low": 30.0,
            "high": 80.0,
        },
        {
            "type": "soil_moisture",
            "unit": "%",
            "desc": "Soil Water Content (D3)",
            "low": 20.0,
            "high": 60.0,
        },
        {
            "type": "light",
            "unit": "Lux",
            "desc": "Ambient Light (D4)",
            "low": 100.0,
            "high": 1000.0,
        },
        {
            "type": "co2",
            "unit": "ppm",
            "desc": "Carbon Dioxide (D5)",
            "low": 400.0,
            "high": 1200.0,
        },
        {
            "type": "cov",
            "unit": "Index",
            "desc": "Volatile Organic Comp. (D6)",
            "low": 0.0,
            "high": 150.0,
        },
        {
            "type": "nox",
            "unit": "Index",
            "desc": "Nitrogen Oxides (D7)",
            "low": 0.0,
            "high": 50.0,
        },
    ]
    existing_sensors = DatabaseManager.get_sensors()
    if not existing_sensors:
        created_sensors = []
        current_parcels = DatabaseManager.get_parcels()
        for parcel in current_parcels:
            pid = parcel["id"]
            p_name = parcel["name"]
            if "Greenhouse" in p_name:
                logger.info(
                    f"Seeding full sensor suite for {p_name} (MAIoTA Target)..."
                )
                for tpl in sensor_templates:
                    sid = DatabaseManager.create_sensor(
                        parcel_id=pid,
                        type_=tpl["type"],
                        unit=tpl["unit"],
                        description=f"{tpl['desc']} (MAIoTA)",
                        threshold_low=tpl["low"],
                        threshold_high=tpl["high"],
                    )
                    created_sensors.append(
                        {
                            "id": sid,
                            "type": tpl["type"],
                            "low": tpl["low"],
                            "high": tpl["high"],
                        }
                    )
                    logger.info(f"Created {tpl['type']} sensor {sid} for {p_name}")
            else:
                for _ in range(random.randint(2, 3)):
                    tpl = random.choice(sensor_templates)
                    sid = DatabaseManager.create_sensor(
                        parcel_id=pid,
                        type_=tpl["type"],
                        unit=tpl["unit"],
                        description=f"{tpl['desc']} - Unit {random.randint(1, 99)}",
                        threshold_low=tpl["low"],
                        threshold_high=tpl["high"],
                    )
                    created_sensors.append(
                        {
                            "id": sid,
                            "type": tpl["type"],
                            "low": tpl["low"],
                            "high": tpl["high"],
                        }
                    )
                    logger.info(f"Created sensor {sid} for parcel {pid}")
    else:
        created_sensors = []
        for s in existing_sensors:
            created_sensors.append(
                {
                    "id": s["id"],
                    "type": s["type"],
                    "low": s["threshold_low"],
                    "high": s["threshold_high"],
                }
            )
        logger.info("Sensors already exist, using existing IDs.")
    logger.info("Generating historical sensor data...")
    now = datetime.now()
    if created_sensors and (
        not DatabaseManager.get_sensor_data(created_sensors[0]["id"])
    ):
        count = 0
        for sensor in created_sensors:
            base_val = 25.0 if sensor["type"] == "temperature" else 50.0
            for hour_delta in range(24, 0, -1):
                timestamp = (now - timedelta(hours=hour_delta)).isoformat()
                noise = random.uniform(-5, 5)
                val = base_val + noise
                if random.random() < 0.05:
                    val += 20
                DatabaseManager.insert_sensor_data(
                    sensor_id=sensor["id"],
                    value=round(val, 2),
                    raw=f"RAW_{int(val * 100)}",
                    timestamp=timestamp,
                )
                count += 1
                if sensor["high"] and val > sensor["high"]:
                    DatabaseManager.create_alert(
                        sensor_id=sensor["id"],
                        type_="THRESHOLD_HIGH",
                        message=f"Value {val:.2f} exceeded high threshold {sensor['high']}",
                        timestamp=timestamp,
                    )
                elif sensor["low"] and val < sensor["low"]:
                    DatabaseManager.create_alert(
                        sensor_id=sensor["id"],
                        type_="THRESHOLD_LOW",
                        message=f"Value {val:.2f} below low threshold {sensor['low']}",
                        timestamp=timestamp,
                    )
        logger.info(f"Inserted {count} data points.")
    else:
        logger.info(
            "Sensor data already exists or no sensors found. Skipping data generation."
        )
    logger.info("Agrotech Database Seeding Complete.")


if __name__ == "__main__":
    seed_agrotech_db()