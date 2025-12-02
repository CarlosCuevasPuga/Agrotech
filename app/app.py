import reflex as rx
from fastapi import FastAPI
from app.pages.login import login_page
from app.pages.dashboard import dashboard
from app.states.auth_state import AuthState
from app.states.db_state import DatabaseState
from app.states.parcels_state import ParcelsState
from app.api.endpoints import router as api_router


def api_routes(app):
    api = FastAPI()
    api.include_router(api_router)
    app.mount("/api", api)
    return app


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&display=swap"
    ],
    api_transformer=api_routes,
)
app.add_page(login_page, route="/login")
app.add_page(dashboard, route="/", on_load=[AuthState.on_mount, DatabaseState.on_mount])
from app.pages.system import system_page
from app.pages.parcels import parcels_page
from app.pages.sensors_management import sensors_management_page

app.add_page(
    system_page, route="/system", on_load=[AuthState.on_mount, DatabaseState.on_mount]
)
app.add_page(
    parcels_page,
    route="/parcels",
    on_load=[AuthState.on_mount, ParcelsState.load_parcels],
)
app.add_page(
    sensors_management_page,
    route="/parcels/[parcel_id]/sensors",
    on_load=[AuthState.on_mount],
)
from app.pages.analytics import analytics_page
from app.pages.alerts import alerts_page

app.add_page(analytics_page, route="/analytics", on_load=[AuthState.on_mount])
app.add_page(alerts_page, route="/alerts", on_load=[AuthState.on_mount])