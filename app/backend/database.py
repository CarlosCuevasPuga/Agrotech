import sqlite3
import logging
import hashlib
import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DB_FILE_NAME = "agrotech_data.db"


class DatabaseManager:
    """
    Manages SQLite database connections and schema initialization for Agrotech system.
    """

    @staticmethod
    def get_db_path() -> Path:
        """Returns the path to the database file."""
        return Path(DB_FILE_NAME).resolve()

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """
        Establishes and returns a connection to the SQLite database.
        Enables row factory for dictionary-like access.
        """
        try:
            db_path = DatabaseManager.get_db_path()
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.exception(f"Failed to connect to database: {e}")
            raise

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using PBKDF2-HMAC-SHA256 with a random salt.
        Returns string in format 'salt:hash'.
        """
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        return f"{salt}:{pwd_hash.hex()}"

    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        """
        Verifies a provided password against the stored 'salt:hash' string.
        """
        try:
            salt, key_hex = stored_hash.split(":")
            new_key = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return new_key.hex() == key_hex
        except (ValueError, AttributeError) as e:
            logger.exception(f"Password verification failed: {e}")
            return False

    @staticmethod
    def initialize_schema() -> bool:
        """
        Creates the necessary tables for Agrotech system.
        """
        create_users_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        );
        """
        create_parcels_sql = """
        CREATE TABLE IF NOT EXISTS parcels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT
        );
        """
        create_sensors_sql = """
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parcel_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            unit TEXT,
            description TEXT,
            threshold_low REAL,
            threshold_high REAL,
            FOREIGN KEY (parcel_id) REFERENCES parcels (id) ON DELETE CASCADE
        );
        """
        create_sensor_data_sql = """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            value REAL,
            raw TEXT,
            FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
        );
        """
        create_alerts_sql = """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type TEXT,
            message TEXT,
            acknowledged INTEGER DEFAULT 0,
            FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
        );
        """
        create_maiota_sql = """
        CREATE TABLE IF NOT EXISTS maiota_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_key TEXT,
            data_type TEXT,
            value_str TEXT,
            value_num REAL,
            category TEXT,
            timestamp DATETIME,
            metadata TEXT
        );
        """
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(create_users_sql)
                cursor.execute(create_parcels_sql)
                cursor.execute(create_sensors_sql)
                cursor.execute(create_sensor_data_sql)
                cursor.execute(create_alerts_sql)
                cursor.execute(create_maiota_sql)
                conn.commit()
                logger.info("Database schema initialized successfully (Agrotech).")
                return True
        except sqlite3.Error as e:
            logger.exception(f"Database initialization failed: {e}")
            return False

    @staticmethod
    def create_user(username: str, password: str, role: str = "user") -> int:
        password_hash = DatabaseManager.hash_password(password)
        sql = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (username, password_hash, role))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_user_by_username(username: str) -> Optional[dict]:
        sql = "SELECT * FROM users WHERE username = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create_parcel(name: str, location: str) -> int:
        sql = "INSERT INTO parcels (name, location) VALUES (?, ?)"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (name, location))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_parcels() -> list[dict]:
        sql = "SELECT * FROM parcels"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_parcel_by_id(parcel_id: int) -> Optional[dict]:
        sql = "SELECT * FROM parcels WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (parcel_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update_parcel(parcel_id: int, name: str, location: str) -> bool:
        sql = "UPDATE parcels SET name = ?, location = ? WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (name, location, parcel_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_parcel(parcel_id: int) -> bool:
        sql = "DELETE FROM parcels WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (parcel_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def create_sensor(
        parcel_id: int,
        type_: str,
        unit: str,
        description: str,
        threshold_low: float = None,
        threshold_high: float = None,
    ) -> int:
        sql = """
        INSERT INTO sensors (parcel_id, type, unit, description, threshold_low, threshold_high)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (parcel_id, type_, unit, description, threshold_low, threshold_high),
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_sensors() -> list[dict]:
        sql = "SELECT * FROM sensors"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_sensors_by_parcel(parcel_id: int) -> list[dict]:
        sql = "SELECT * FROM sensors WHERE parcel_id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (parcel_id,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_sensor_by_id(sensor_id: int) -> Optional[dict]:
        sql = "SELECT * FROM sensors WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (sensor_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update_sensor(
        sensor_id: int,
        type_: str,
        unit: str,
        description: str,
        threshold_low: float,
        threshold_high: float,
    ) -> bool:
        sql = """
        UPDATE sensors 
        SET type = ?, unit = ?, description = ?, threshold_low = ?, threshold_high = ?
        WHERE id = ?
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (type_, unit, description, threshold_low, threshold_high, sensor_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_sensor(sensor_id: int) -> bool:
        sql = "DELETE FROM sensors WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (sensor_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def insert_sensor_data(
        sensor_id: int, value: float, raw: str = None, timestamp: str = None
    ) -> int:
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        sql = "INSERT INTO sensor_data (sensor_id, value, raw, timestamp) VALUES (?, ?, ?, ?)"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (sensor_id, value, raw, timestamp))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_sensor_data(
        sensor_id: int, limit: int = 100, offset: int = 0
    ) -> list[dict]:
        sql = """
        SELECT * FROM sensor_data 
        WHERE sensor_id = ? 
        ORDER BY timestamp DESC 
        LIMIT ? OFFSET ?
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (sensor_id, limit, offset))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_latest_readings() -> list[dict]:
        """Returns the most recent reading for each sensor."""
        sql = """
        SELECT s.id as sensor_id, s.type, s.parcel_id, sd.value, sd.timestamp, s.unit
        FROM sensors s
        LEFT JOIN (
            SELECT sensor_id, value, timestamp
            FROM sensor_data
            WHERE id IN (
                SELECT MAX(id)
                FROM sensor_data
                GROUP BY sensor_id
            )
        ) sd ON s.id = sd.sensor_id
        """
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def create_alert(
        sensor_id: int, type_: str, message: str, timestamp: str = None
    ) -> int:
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        sql = "INSERT INTO alerts (sensor_id, type, message, timestamp) VALUES (?, ?, ?, ?)"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (sensor_id, type_, message, timestamp))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_alerts(limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def acknowledge_alert(alert_id: int) -> bool:
        sql = "UPDATE alerts SET acknowledged = 1 WHERE id = ?"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (alert_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_unacknowledged_alerts() -> list[dict]:
        sql = "SELECT * FROM alerts WHERE acknowledged = 0 ORDER BY timestamp DESC"
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_filtered_alerts(
        sensor_id: Optional[int] = None,
        type_: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        acknowledged: Optional[bool] = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        Retrieves alerts with advanced filtering options.
        """
        sql = """
        SELECT a.*, s.description as sensor_desc, s.type as sensor_type, p.name as parcel_name
        FROM alerts a 
        LEFT JOIN sensors s ON a.sensor_id = s.id
        LEFT JOIN parcels p ON s.parcel_id = p.id
        WHERE 1=1
        """
        params = []
        if sensor_id is not None and sensor_id != 0:
            sql += " AND a.sensor_id = ?"
            params.append(sensor_id)
        if type_ and type_ != "all":
            sql += " AND a.type = ?"
            params.append(type_)
        if start_date:
            sql += " AND a.timestamp >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND a.timestamp <= ?"
            params.append(end_date)
        if acknowledged is not None:
            sql += " AND a.acknowledged = ?"
            params.append(1 if acknowledged else 0)
        sql += " ORDER BY a.timestamp DESC LIMIT ?"
        params.append(limit)
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def check_status() -> dict:
        """
        Checks the health of the database connection and schema.
        """
        status = {
            "connected": False,
            "table_exists": False,
            "record_count": 0,
            "last_check": datetime.now().isoformat(),
        }
        try:
            with DatabaseManager.get_connection() as conn:
                status["connected"] = True
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='maiota_records';"
                )
                if cursor.fetchone():
                    status["table_exists"] = True
                    cursor.execute("SELECT COUNT(*) FROM maiota_records")
                    status["record_count"] = cursor.fetchone()[0]
        except Exception as e:
            logger.exception(f"Status check failed: {e}")
        return status

    @staticmethod
    def insert_batch(records: list[dict]) -> int:
        sql = """
        INSERT INTO maiota_records (source_key, data_type, value_str, value_num, category, timestamp, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        data = [
            (
                r["source_key"],
                r["data_type"],
                r["value_str"],
                r["value_num"],
                r["category"],
                r["timestamp"],
                r["metadata"],
            )
            for r in records
        ]
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(sql, data)
            conn.commit()
            return cursor.rowcount

    @staticmethod
    def fetch_records(limit: int, offset: int, search_query: str = "") -> list[dict]:
        if search_query:
            sql = """
            SELECT * FROM maiota_records 
            WHERE source_key LIKE ? OR category LIKE ?
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
            """
            params = (f"%{search_query}%", f"%{search_query}%", limit, offset)
        else:
            sql = (
                "SELECT * FROM maiota_records ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            )
            params = (limit, offset)
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def count_records(search_query: str = "") -> int:
        if search_query:
            sql = "SELECT COUNT(*) FROM maiota_records WHERE source_key LIKE ? OR category LIKE ?"
            params = (f"%{search_query}%", f"%{search_query}%")
        else:
            sql = "SELECT COUNT(*) FROM maiota_records"
            params = ()
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return cursor.fetchone()[0]

    @staticmethod
    def get_sensor_data_history(
        sensor_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict]:
        """
        Retrieves historical sensor data with optional date filtering.
        """
        sql = "SELECT * FROM sensor_data WHERE sensor_id = ?"
        params = [sensor_id]
        if start_date:
            sql += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            sql += " AND timestamp <= ?"
            params.append(end_date)
        sql += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        with DatabaseManager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, tuple(params))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_sensor_history_batch(limit: int = 20) -> dict[int, list[dict]]:
        """
        Retrieves recent history for all sensors to display sparklines.
        Returns a dict mapping sensor_id to a list of data points.
        """
        sql = """
        SELECT sensor_id, value, timestamp 
        FROM (
            SELECT sensor_id, value, timestamp,
            ROW_NUMBER() OVER (PARTITION BY sensor_id ORDER BY timestamp DESC) as rn
            FROM sensor_data
        ) 
        WHERE rn <= ?
        ORDER BY timestamp ASC
        """
        history_map = {}
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (limit,))
                rows = cursor.fetchall()
                for row in rows:
                    sid = row["sensor_id"]
                    if sid not in history_map:
                        history_map[sid] = []
                    history_map[sid].append(
                        {"value": row["value"], "timestamp": row["timestamp"]}
                    )
            return history_map
        except Exception as e:
            logger.exception(f"Failed to get batch history: {e}")
            return {}

    @staticmethod
    def get_system_stats() -> dict:
        """
        Returns aggregated system statistics for the dashboard API.
        """
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM parcels")
                parcels_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM sensors")
                sensors_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM alerts WHERE acknowledged = 0")
                alerts_count = cursor.fetchone()[0]
                return {
                    "parcels_count": parcels_count,
                    "sensors_count": sensors_count,
                    "active_alerts_count": alerts_count,
                }
        except Exception as e:
            logger.exception(f"Failed to get system stats: {e}")
            return {"parcels_count": 0, "sensors_count": 0, "active_alerts_count": 0}