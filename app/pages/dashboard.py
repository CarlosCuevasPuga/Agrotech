import reflex as rx
from app.states.sensors_state import SensorsState
from app.components.dashboard_components import parcel_section, alerts_panel
from app.components.navbar import navbar


def dashboard() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Farm Overview",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.button(
                            rx.cond(
                                SensorsState.is_loading,
                                rx.icon("loader", class_name="w-4 h-4 animate-spin"),
                                rx.icon("refresh-cw", class_name="w-4 h-4"),
                            ),
                            on_click=SensorsState.fetch_dashboard_data,
                            class_name="p-2 rounded-full hover:bg-gray-200 transition-colors text-gray-600",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.cond(
                                SensorsState.parcels_data.length() > 0,
                                rx.foreach(SensorsState.parcels_data, parcel_section),
                                rx.el.div(
                                    rx.icon(
                                        "sprout",
                                        class_name="w-12 h-12 text-gray-300 mb-4",
                                    ),
                                    rx.el.p(
                                        "No parcels found or loading data...",
                                        class_name="text-gray-500",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-20 bg-white rounded-2xl border border-dashed border-gray-300",
                                ),
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(alerts_panel(), class_name="w-full lg:w-80 shrink-0"),
                        class_name="flex flex-col lg:flex-row gap-6 items-start",
                    ),
                    class_name="container mx-auto px-4 py-8",
                ),
                class_name="pb-20",
            ),
            class_name="min-h-screen bg-gray-50",
        ),
        rx.el.div(on_mount=SensorsState.on_mount),
        class_name="font-['Inter']",
    )