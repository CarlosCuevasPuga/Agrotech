from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import logging
from app.backend.database import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()


class SensorDataIngest(BaseModel):
    value: float
    timestamp: Optional[str] = None
    raw: Optional[str] = None


class SensorDataResponse(BaseModel):
    id: int
    status: str
    message: str


class ParcelResponse(BaseModel):
    id: int
    name: str
    location: str


@router.post("/sensors/{sensor_id}/data", response_model=SensorDataResponse)
async def ingest_sensor_data(sensor_id: int, payload: SensorDataIngest):
    """
    Ingest data for a specific sensor.

    - Validates sensor existence.
    - Checks thresholds and automatically creates alerts.
    - Inserts data record.
    """
    sensor = DatabaseManager.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=404, detail=f"Sensor with ID {sensor_id} not found."
        )
    val = payload.value
    timestamp = payload.timestamp or datetime.now().isoformat()
    if sensor["threshold_high"] is not None and val > sensor["threshold_high"]:
        DatabaseManager.create_alert(
            sensor_id=sensor_id,
            type_="THRESHOLD_HIGH",
            message=f"Value {val} exceeded high threshold {sensor['threshold_high']}",
            timestamp=timestamp,
        )
    elif sensor["threshold_low"] is not None and val < sensor["threshold_low"]:
        DatabaseManager.create_alert(
            sensor_id=sensor_id,
            type_="THRESHOLD_LOW",
            message=f"Value {val} dropped below low threshold {sensor['threshold_low']}",
            timestamp=timestamp,
        )
    try:
        record_id = DatabaseManager.insert_sensor_data(
            sensor_id=sensor_id, value=val, raw=payload.raw, timestamp=timestamp
        )
        return {
            "id": record_id,
            "status": "success",
            "message": "Data ingested successfully.",
        }
    except Exception as e:
        logger.exception(f"Failed to ingest data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to ingest data: {str(e)}")


@router.get("/sensors/{sensor_id}/data")
async def get_sensor_history(
    sensor_id: int,
    start_date: Optional[str] = Query(
        None, alias="from", description="Start date (ISO 8601)"
    ),
    end_date: Optional[str] = Query(
        None, alias="to", description="End date (ISO 8601)"
    ),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
):
    """
    Get historical data for a sensor with optional date filtering.
    """
    sensor = DatabaseManager.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=404, detail=f"Sensor with ID {sensor_id} not found."
        )
    try:
        data = DatabaseManager.get_sensor_data_history(
            sensor_id, start_date, end_date, limit
        )
        return data
    except Exception as e:
        logger.exception(f"Failed to get sensor history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/parcels", response_model=list[ParcelResponse])
async def list_parcels():
    """
    List all registered parcels.
    """
    return DatabaseManager.get_parcels()


@router.get("/parcels/{id}/sensors")
async def get_parcel_sensors(id: int):
    """
    Get all sensors associated with a specific parcel.
    """
    parcel = DatabaseManager.get_parcel_by_id(id)
    if not parcel:
        raise HTTPException(status_code=404, detail=f"Parcel with ID {id} not found.")
    return DatabaseManager.get_sensors_by_parcel(id)


@router.get("/dashboard")
async def get_dashboard_summary():
    """
    Get a summary for the main dashboard:
    - Latest readings for all sensors
    - Unacknowledged alerts
    - System statistics
    """
    try:
        latest_readings = DatabaseManager.get_latest_readings()
        active_alerts = DatabaseManager.get_unacknowledged_alerts()
        stats = DatabaseManager.get_system_stats()
        return {
            "stats": stats,
            "latest_readings": latest_readings,
            "active_alerts": active_alerts,
        }
    except Exception as e:
        logger.exception(f"Failed to get dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))