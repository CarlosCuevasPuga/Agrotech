import reflex as rx
from datetime import datetime, timedelta
import logging
from app.backend.database import DatabaseManager
from app.models.data_models import Sensor

logger = logging.getLogger(__name__)


class AnalyticsState(rx.State):
    sensors: list[Sensor] = []
    selected_sensor_id: str = ""
    start_date: str = (datetime.now() - timedelta(days=1)).isoformat().split("T")[0]
    end_date: str = datetime.now().isoformat().split("T")[0]
    chart_data: list[dict] = []
    is_loading: bool = False

    @rx.event
    def load_initial_data(self):
        self.sensors = DatabaseManager.get_sensors()
        if self.sensors and (not self.selected_sensor_id):
            self.selected_sensor_id = str(self.sensors[0]["id"])
        self.load_history()

    @rx.event
    def set_sensor(self, value: str):
        self.selected_sensor_id = value
        self.load_history()

    @rx.event
    def set_start_date(self, value: str):
        self.start_date = value
        self.load_history()

    @rx.event
    def set_end_date(self, value: str):
        self.end_date = value
        self.load_history()

    @rx.event
    async def load_history(self):
        if not self.selected_sensor_id:
            return
        self.is_loading = True
        yield
        try:
            s_id = int(self.selected_sensor_id)
        except ValueError as e:
            logger.exception(f"Invalid sensor ID: {e}")
            self.is_loading = False
            return
        s_ts = f"{self.start_date}T00:00:00"
        e_ts = f"{self.end_date}T23:59:59"
        try:
            data = DatabaseManager.get_sensor_data_history(
                s_id, start_date=s_ts, end_date=e_ts, limit=500
            )
            self.chart_data = sorted(data, key=lambda x: x["timestamp"])
        except Exception as e:
            logger.exception(f"Failed to load history: {e}")
            self.chart_data = []
        self.is_loading = False