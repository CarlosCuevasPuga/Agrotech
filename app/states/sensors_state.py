import reflex as rx
import asyncio
import logging
from datetime import datetime
from app.backend.database import DatabaseManager
from app.models.data_models import EnrichedParcel, Alert


class SensorsState(rx.State):
    """
    Manages the state for sensor data, dashboard metrics, and alerts.
    """

    parcels_data: list[EnrichedParcel] = []
    active_alerts: list[Alert] = []
    is_loading: bool = False
    last_updated: str = "-"
    auto_refresh_active: bool = True

    @rx.event
    async def fetch_dashboard_data(self):
        """
        Fetches all necessary data for the dashboard:
        - Parcels and their sensors
        - Latest readings
        - Sparkline history
        - Active alerts
        """
        self.is_loading = True
        yield
        try:
            parcels = DatabaseManager.get_parcels()
            all_sensors = DatabaseManager.get_sensors()
            latest_readings = DatabaseManager.get_latest_readings()
            readings_map = {r["sensor_id"]: r for r in latest_readings}
            history_map = DatabaseManager.get_sensor_history_batch(limit=20)
            self.active_alerts = DatabaseManager.get_unacknowledged_alerts()
            enriched_parcels = []
            for p in parcels:
                p_id = p["id"]
                p_sensors = [s for s in all_sensors if s["parcel_id"] == p_id]
                enriched_sensors = []
                for s in p_sensors:
                    s_id = s["id"]
                    reading = readings_map.get(s_id)
                    history = history_map.get(s_id, [])
                    status = "inactive"
                    status_color = "gray"
                    val = None
                    if reading:
                        val = reading["value"]
                        status = "active"
                        status_color = "green"
                        if (
                            val is not None
                            and s["threshold_high"] is not None
                            and (val > s["threshold_high"])
                        ):
                            status = "critical"
                            status_color = "red"
                        elif (
                            val is not None
                            and s["threshold_low"] is not None
                            and (val < s["threshold_low"])
                        ):
                            status = "warning"
                            status_color = "yellow"
                    enriched_sensors.append(
                        {
                            **s,
                            "current_value": val,
                            "latest_timestamp": reading["timestamp"]
                            if reading
                            else None,
                            "status": status,
                            "status_color": status_color,
                            "history": history,
                        }
                    )
                enriched_parcels.append({**p, "sensors": enriched_sensors})
            self.parcels_data = enriched_parcels
            self.last_updated = datetime.now().strftime("%H:%M:%S")
        except Exception as e:
            logging.exception(f"Dashboard fetch error: {e}")
        self.is_loading = False

    @rx.event
    async def on_mount(self):
        """Initial load and start timer."""
        yield SensorsState.fetch_dashboard_data
        yield SensorsState.tick

    @rx.event
    async def tick(self):
        """Background task for auto-refresh."""
        if self.auto_refresh_active:
            await asyncio.sleep(30)
            yield SensorsState.fetch_dashboard_data
            yield SensorsState.tick

    @rx.event
    def acknowledge_alert(self, alert_id: int):
        """Marks an alert as acknowledged."""
        DatabaseManager.acknowledge_alert(alert_id)
        return SensorsState.fetch_dashboard_data