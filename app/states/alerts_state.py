import reflex as rx
from datetime import datetime, timedelta
import logging
from app.backend.database import DatabaseManager
from app.models.data_models import Sensor, EnrichedAlert

logger = logging.getLogger(__name__)


class AlertsState(rx.State):
    alerts: list[EnrichedAlert] = []
    sensors: list[Sensor] = []
    filter_sensor_id: str = "0"
    filter_type: str = "all"
    filter_acknowledged: str = "unacknowledged"
    total_alerts: int = 0
    pending_alerts: int = 0
    is_loading: bool = False

    @rx.event
    def load_initial_data(self):
        self.sensors = DatabaseManager.get_sensors()
        self.load_alerts()

    @rx.event
    def set_filter_sensor(self, value: str):
        self.filter_sensor_id = value
        self.load_alerts()

    @rx.event
    def set_filter_type(self, value: str):
        self.filter_type = value
        self.load_alerts()

    @rx.event
    def set_filter_acknowledged(self, value: str):
        self.filter_acknowledged = value
        self.load_alerts()

    @rx.event
    async def load_alerts(self):
        self.is_loading = True
        yield
        try:
            sid = int(self.filter_sensor_id) if self.filter_sensor_id.isdigit() else 0
            ack_filter = None
            if self.filter_acknowledged == "acknowledged":
                ack_filter = True
            elif self.filter_acknowledged == "unacknowledged":
                ack_filter = False
            self.alerts = DatabaseManager.get_filtered_alerts(
                sensor_id=sid,
                type_=self.filter_type,
                acknowledged=ack_filter,
                limit=100,
            )
            self.total_alerts = len(self.alerts)
            unacked = DatabaseManager.get_unacknowledged_alerts()
            self.pending_alerts = len(unacked)
        except Exception as e:
            logger.exception(f"Failed to load alerts: {e}")
            self.alerts = []
        self.is_loading = False

    @rx.event
    def acknowledge_alert(self, alert_id: int):
        try:
            DatabaseManager.acknowledge_alert(alert_id)
            self.load_alerts()
        except Exception as e:
            logger.exception(f"Failed to ack alert: {e}")