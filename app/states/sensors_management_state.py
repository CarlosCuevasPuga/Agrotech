import reflex as rx
import logging
from app.backend.database import DatabaseManager
from app.models.data_models import Sensor, Parcel

logger = logging.getLogger(__name__)


class SensorsManagementState(rx.State):
    current_parcel_id: int = 0
    current_parcel: Parcel | None = None
    sensors: list[Sensor] = []
    is_modal_open: bool = False
    is_delete_modal_open: bool = False
    editing_sensor: Sensor | None = None
    form_type: str = ""
    form_unit: str = ""
    form_description: str = ""
    form_threshold_low: str = ""
    form_threshold_high: str = ""
    form_error: str = ""

    @rx.event
    def load_data(self):
        args = self.router.page.params
        pid_str = args.get("parcel_id", "0")
        if isinstance(pid_str, list):
            pid_str = pid_str[0] if pid_str else "0"
        try:
            self.current_parcel_id = int(pid_str)
        except ValueError as e:
            logger.exception(f"Invalid parcel_id: {e}")
            self.current_parcel_id = 0
        self.current_parcel = DatabaseManager.get_parcel_by_id(self.current_parcel_id)
        self.load_sensors()

    @rx.event
    def load_sensors(self):
        if self.current_parcel_id:
            self.sensors = DatabaseManager.get_sensors_by_parcel(self.current_parcel_id)

    @rx.event
    def open_add_modal(self):
        self.editing_sensor = None
        self.form_type = "temperature"
        self.form_unit = "°C"
        self.form_description = ""
        self.form_threshold_low = ""
        self.form_threshold_high = ""
        self.form_error = ""
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, sensor: Sensor):
        self.editing_sensor = sensor
        self.form_type = sensor["type"]
        self.form_unit = sensor["unit"]
        self.form_description = sensor["description"]
        self.form_threshold_low = (
            str(sensor["threshold_low"]) if sensor["threshold_low"] is not None else ""
        )
        self.form_threshold_high = (
            str(sensor["threshold_high"])
            if sensor["threshold_high"] is not None
            else ""
        )
        self.form_error = ""
        self.is_modal_open = True

    @rx.event
    def open_delete_modal(self, sensor: Sensor):
        self.editing_sensor = sensor
        self.is_delete_modal_open = True

    @rx.event
    def close_modals(self):
        self.is_modal_open = False
        self.is_delete_modal_open = False
        self.editing_sensor = None
        self.form_error = ""

    @rx.event
    def save_sensor(self):
        if not self.form_type or not self.form_unit:
            self.form_error = "Type and Unit are required."
            return
        try:
            low = (
                float(self.form_threshold_low)
                if self.form_threshold_low.strip()
                else None
            )
            high = (
                float(self.form_threshold_high)
                if self.form_threshold_high.strip()
                else None
            )
        except ValueError as e:
            logger.exception(f"Error parsing thresholds: {e}")
            self.form_error = "Thresholds must be valid numbers."
            return
        try:
            if self.editing_sensor:
                DatabaseManager.update_sensor(
                    sensor_id=self.editing_sensor["id"],
                    type_=self.form_type,
                    unit=self.form_unit,
                    description=self.form_description,
                    threshold_low=low,
                    threshold_high=high,
                )
            else:
                DatabaseManager.create_sensor(
                    parcel_id=self.current_parcel_id,
                    type_=self.form_type,
                    unit=self.form_unit,
                    description=self.form_description,
                    threshold_low=low,
                    threshold_high=high,
                )
            self.close_modals()
            self.load_sensors()
        except Exception as e:
            logger.exception(f"Error saving sensor: {e}")
            self.form_error = str(e)

    @rx.event
    def delete_sensor(self):
        if self.editing_sensor:
            DatabaseManager.delete_sensor(self.editing_sensor["id"])
            self.close_modals()
            self.load_sensors()