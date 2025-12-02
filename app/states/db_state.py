import reflex as rx
import asyncio
import logging
from datetime import datetime
from app.backend.database import DatabaseManager
from app.backend.MAIoTALib import MAIOTA_DATA
from app.models.data_models import DatabaseStatus, MaiotaRecord


class DatabaseState(rx.State):
    """
    State management for Database operations.
    """

    is_initialized: bool = False
    is_loading: bool = False
    status: DatabaseStatus = {
        "connected": False,
        "table_exists": False,
        "record_count": 0,
        "last_check": "",
    }
    logs: list[str] = []
    records: list[MaiotaRecord] = []
    search_query: str = ""
    page: int = 1
    page_size: int = 10
    total_records: int = 0

    @rx.var
    def total_pages(self) -> int:
        return (self.total_records + self.page_size - 1) // self.page_size

    @rx.var
    def has_next_page(self) -> bool:
        return self.page < self.total_pages

    @rx.var
    def has_prev_page(self) -> bool:
        return self.page > 1

    @rx.event
    async def load_records(self):
        """Fetches records based on current page and search query."""
        status = DatabaseManager.check_status()
        if not status["table_exists"]:
            self.records = []
            self.total_records = 0
            return
        try:
            offset = (self.page - 1) * self.page_size
            self.records = DatabaseManager.fetch_records(
                limit=self.page_size, offset=offset, search_query=self.search_query
            )
            self.total_records = DatabaseManager.count_records(self.search_query)
        except Exception as e:
            logging.exception(f"Error loading records: {e}")
            self._add_log(f"Error loading records: {str(e)}")

    @rx.event
    def set_search_query(self, query: str):
        """Updates search query and resets to first page."""
        self.search_query = query
        self.page = 1
        return DatabaseState.load_records

    @rx.event
    def next_page(self):
        if self.has_next_page:
            self.page += 1
            return DatabaseState.load_records

    @rx.event
    def prev_page(self):
        if self.has_prev_page:
            self.page -= 1
            return DatabaseState.load_records

    def _add_log(self, message: str):
        self.logs.insert(0, f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        if len(self.logs) > 10:
            self.logs.pop()

    @rx.event
    async def check_connection(self):
        """Checks the database status without modifying it."""
        self.is_loading = True
        await asyncio.sleep(0.5)
        try:
            current_status = DatabaseManager.check_status()
            self.status = current_status
            if current_status["connected"]:
                self._add_log("Connection check: Success")
            else:
                self._add_log("Connection check: Failed")
        except Exception as e:
            logging.exception(f"Error checking connection: {e}")
            self._add_log(f"Error checking connection: {str(e)}")
        self.is_loading = False

    @rx.event
    async def initialize_database(self):
        """Initializes the database schema."""
        self.is_loading = True
        self._add_log("Starting initialization...")
        await asyncio.sleep(0.8)
        try:
            success = DatabaseManager.initialize_schema()
            if success:
                self.is_initialized = True
                self._add_log("Schema created successfully.")
                self.status = DatabaseManager.check_status()
            else:
                self._add_log("Schema creation failed.")
        except Exception as e:
            logging.exception(f"Critical Error: {e}")
            self._add_log(f"Critical Error: {str(e)}")
        self.is_loading = False

    @rx.event
    async def import_maiota_data(self):
        """Imports data from MAIoTALib into the database."""
        self.is_loading = True
        self._add_log("Reading data from MAIoTALib...")
        yield
        await asyncio.sleep(0.5)
        try:
            raw_data = MAIOTA_DATA
            if not raw_data:
                self._add_log("Warning: MAIoTALib file is empty.")
                self.is_loading = False
                return
            self._add_log(f"Loaded {len(raw_data)} records from file.")
            valid_records = []
            for rec in raw_data:
                if "source_key" in rec and "category" in rec:
                    valid_records.append(rec)
            skipped = len(raw_data) - len(valid_records)
            if skipped > 0:
                self._add_log(f"Validation: Skipped {skipped} invalid records.")
            status = DatabaseManager.check_status()
            if not status["table_exists"]:
                self._add_log("Table not found. Auto-initializing schema...")
                if DatabaseManager.initialize_schema():
                    self._add_log("Schema auto-initialized.")
                    self.is_initialized = True
                else:
                    self._add_log("Failed to auto-initialize schema.")
                    self.is_loading = False
                    return
            if valid_records:
                inserted_count = DatabaseManager.insert_batch(valid_records)
                self._add_log(f"Success: Inserted {inserted_count} records to DB.")
                self.status = DatabaseManager.check_status()
            else:
                self._add_log("Error: No valid records to insert.")
        except Exception as e:
            logging.exception(f"Import failed: {e}")
            self._add_log(f"Import Error: {str(e)}")
        self.is_loading = False
        yield DatabaseState.load_records
        return

    @rx.event
    async def on_mount(self):
        """Run on page load. Checks connection and loads records if possible."""
        self.is_loading = True
        try:
            current_status = DatabaseManager.check_status()
            self.status = current_status
            if current_status["connected"]:
                self._add_log("Connection check: Success")
            if current_status["table_exists"]:
                yield DatabaseState.load_records
            else:
                self._add_log("Database table not found. Auto-initializing...")
                if DatabaseManager.initialize_schema():
                    self._add_log("Schema initialized automatically on mount.")
                    self.is_initialized = True
                    self.status = DatabaseManager.check_status()
                    yield DatabaseState.load_records
                else:
                    self._add_log("Failed to initialize database on mount.")
        except Exception as e:
            logging.exception(f"On mount error: {e}")
            self._add_log(f"On mount error: {str(e)}")
        self.is_loading = False