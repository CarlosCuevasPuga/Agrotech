import reflex as rx
from typing import TypedDict, Optional


class User(TypedDict):
    id: Optional[int]
    username: str
    role: str


class Parcel(TypedDict):
    id: Optional[int]
    name: str
    location: str


class Sensor(TypedDict):
    id: Optional[int]
    parcel_id: int
    type: str
    unit: str
    description: str
    threshold_low: Optional[float]
    threshold_high: Optional[float]


class SensorData(TypedDict):
    id: Optional[int]
    sensor_id: int
    timestamp: str
    value: float
    raw: Optional[str]


class Alert(TypedDict):
    id: Optional[int]
    sensor_id: int
    timestamp: str
    type: str
    message: str
    acknowledged: bool


class DatabaseStatus(TypedDict):
    connected: bool
    table_exists: bool
    record_count: int
    last_check: str


class MaiotaRecord(TypedDict):
    source_key: str
    data_type: str
    value_str: str
    value_num: float
    category: str
    timestamp: str
    metadata: str


class SensorHistoryPoint(TypedDict):
    value: float
    timestamp: str


class EnrichedSensor(Sensor):
    current_value: Optional[float]
    latest_timestamp: Optional[str]
    status: str
    status_color: str
    history: list[SensorHistoryPoint]


class EnrichedParcel(Parcel):
    sensors: list[EnrichedSensor]


class EnrichedAlert(Alert):
    sensor_desc: str
    sensor_type: str
    parcel_name: str