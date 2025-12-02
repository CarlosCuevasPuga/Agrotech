import reflex as rx
import logging
from app.backend.database import DatabaseManager
from app.models.data_models import Parcel

logger = logging.getLogger(__name__)


class ParcelsState(rx.State):
    parcels: list[Parcel] = []
    filtered_parcels: list[Parcel] = []
    search_query: str = ""
    is_modal_open: bool = False
    is_delete_modal_open: bool = False
    editing_parcel: Parcel | None = None
    form_name: str = ""
    form_location: str = ""
    form_error: str = ""

    @rx.event
    def load_parcels(self):
        self.parcels = DatabaseManager.get_parcels()
        self.filter_parcels()

    @rx.event
    def filter_parcels(self):
        if self.search_query == "":
            self.filtered_parcels = self.parcels
        else:
            query = self.search_query.lower()
            self.filtered_parcels = [
                p
                for p in self.parcels
                if query in p["name"].lower() or query in p["location"].lower()
            ]

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.filter_parcels()

    @rx.event
    def open_add_modal(self):
        self.editing_parcel = None
        self.form_name = ""
        self.form_location = ""
        self.form_error = ""
        self.is_modal_open = True

    @rx.event
    def open_edit_modal(self, parcel: Parcel):
        self.editing_parcel = parcel
        self.form_name = parcel["name"]
        self.form_location = parcel["location"]
        self.form_error = ""
        self.is_modal_open = True

    @rx.event
    def open_delete_modal(self, parcel: Parcel):
        self.editing_parcel = parcel
        self.is_delete_modal_open = True

    @rx.event
    def close_modals(self):
        self.is_modal_open = False
        self.is_delete_modal_open = False
        self.editing_parcel = None
        self.form_error = ""

    @rx.event
    def save_parcel(self):
        if not self.form_name or not self.form_location:
            self.form_error = "Name and Location are required."
            return
        try:
            if self.editing_parcel:
                success = DatabaseManager.update_parcel(
                    self.editing_parcel["id"], self.form_name, self.form_location
                )
                if not success:
                    self.form_error = "Failed to update parcel."
                    return
            else:
                DatabaseManager.create_parcel(self.form_name, self.form_location)
            self.close_modals()
            self.load_parcels()
        except Exception as e:
            logger.exception(f"Error saving parcel: {e}")
            self.form_error = str(e)

    @rx.event
    def delete_parcel(self):
        if self.editing_parcel:
            DatabaseManager.delete_parcel(self.editing_parcel["id"])
            self.close_modals()
            self.load_parcels()