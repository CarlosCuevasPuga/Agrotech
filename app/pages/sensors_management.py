import reflex as rx
from app.components.navbar import navbar
from app.states.sensors_management_state import SensorsManagementState
from app.components.sensor_forms import sensor_form_modal, delete_sensor_modal
from app.models.data_models import Sensor


def sensor_row(sensor: Sensor) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("activity", class_name="w-4 h-4 text-indigo-500 mr-3"),
                rx.el.div(
                    rx.el.p(
                        sensor["type"].upper(),
                        class_name="font-bold text-xs text-gray-500 uppercase",
                    ),
                    rx.el.p(
                        sensor["description"], class_name="font-medium text-gray-900"
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                sensor["unit"],
                class_name="bg-gray-100 text-gray-600 px-2 py-1 rounded text-sm font-mono",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Low: ", class_name="text-gray-400 text-xs uppercase mr-1"
                    ),
                    rx.cond(
                        sensor["threshold_low"] != None,
                        rx.el.span(
                            sensor["threshold_low"],
                            class_name="font-mono text-gray-700",
                        ),
                        rx.el.span("--", class_name="text-gray-300"),
                    ),
                    class_name="mr-4",
                ),
                rx.el.div(
                    rx.el.span(
                        "High: ", class_name="text-gray-400 text-xs uppercase mr-1"
                    ),
                    rx.cond(
                        sensor["threshold_high"] != None,
                        rx.el.span(
                            sensor["threshold_high"],
                            class_name="font-mono text-gray-700",
                        ),
                        rx.el.span("--", class_name="text-gray-300"),
                    ),
                ),
                class_name="flex items-center text-sm",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: SensorsManagementState.open_edit_modal(sensor),
                    class_name="p-2 text-gray-500 hover:bg-gray-100 hover:text-blue-600 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: SensorsManagementState.open_delete_modal(sensor),
                    class_name="p-2 text-gray-500 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors",
                ),
                class_name="flex items-center justify-end gap-1",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="bg-white hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors",
    )


def sensors_management_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon("arrow-left", class_name="w-4 h-4 mr-2"),
                        "Back to Parcels",
                        href="/parcels",
                        class_name="flex items-center text-gray-500 hover:text-gray-900 transition-colors mb-6 w-fit",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h1(
                                rx.cond(
                                    SensorsManagementState.current_parcel,
                                    SensorsManagementState.current_parcel["name"],
                                    "Parcel Sensors",
                                ),
                                class_name="text-2xl font-bold text-gray-900",
                            ),
                            rx.el.p(
                                rx.cond(
                                    SensorsManagementState.current_parcel,
                                    SensorsManagementState.current_parcel["location"],
                                    "Loading...",
                                ),
                                class_name="text-gray-500",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("plus", class_name="w-4 h-4 mr-2"),
                            "Add Sensor",
                            on_click=SensorsManagementState.open_add_modal,
                            class_name="flex items-center bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors shadow-sm font-medium",
                        ),
                        class_name="flex justify-between items-start mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Sensor Info",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Unit",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Thresholds",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Actions",
                                    class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(SensorsManagementState.sensors, sensor_row)
                        ),
                        class_name="min-w-full",
                    ),
                    rx.cond(
                        SensorsManagementState.sensors.length() == 0,
                        rx.el.div(
                            rx.icon(
                                "cpu", class_name="w-12 h-12 text-gray-300 mb-3 mx-auto"
                            ),
                            rx.el.p(
                                "No sensors configured",
                                class_name="text-gray-500 font-medium text-center",
                            ),
                            rx.el.p(
                                "Add sensors to start monitoring this parcel.",
                                class_name="text-sm text-gray-400 text-center",
                            ),
                            class_name="py-12 flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
                ),
                class_name="container mx-auto px-4 py-8 max-w-5xl",
            ),
            class_name="min-h-screen bg-gray-50 pb-20",
        ),
        sensor_form_modal(),
        delete_sensor_modal(),
        rx.el.div(on_mount=SensorsManagementState.load_data),
        class_name="font-['Inter']",
    )