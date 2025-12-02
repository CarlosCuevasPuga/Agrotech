import reflex as rx
from app.states.auth_state import AuthState
from app.states.sensors_state import SensorsState


def navbar_link(icon: str, text: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="w-4 h-4 mr-2"),
        text,
        href=url,
        class_name="flex items-center text-sm text-gray-300 hover:text-white hover:bg-gray-800 px-3 py-1.5 rounded-lg transition-colors mr-2",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("leaf", class_name="w-6 h-6 text-emerald-400 mr-2"),
                    rx.el.span(
                        "Agrotech Monitor", class_name="text-xl font-bold text-white"
                    ),
                    class_name="flex items-center",
                    href="/",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "Updated: ",
                            class_name="text-gray-400 text-xs uppercase tracking-wide",
                        ),
                        rx.el.span(
                            SensorsState.last_updated,
                            class_name="text-white text-sm font-mono ml-1",
                        ),
                        class_name="mr-6 flex items-center hidden md:flex",
                    ),
                    rx.el.span(
                        f"User: {AuthState.logged_in_user['username']}",
                        class_name="text-gray-300 mr-4 text-sm hidden md:block",
                    ),
                    navbar_link("layout-dashboard", "Dashboard", "/"),
                    navbar_link("map", "Parcels", "/parcels"),
                    navbar_link("line-chart", "Analytics", "/analytics"),
                    navbar_link("bell", "Alerts", "/alerts"),
                    navbar_link("settings", "System", "/system"),
                    rx.el.button(
                        rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="flex items-center text-sm bg-gray-800 hover:bg-gray-700 text-white px-3 py-1.5 rounded-lg transition-colors border border-gray-700 ml-2",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center h-16",
            ),
            class_name="container mx-auto px-4",
        ),
        class_name="bg-gray-900 shadow-lg sticky top-0 z-50",
    )