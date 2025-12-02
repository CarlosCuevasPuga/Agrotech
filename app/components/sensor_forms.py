import reflex as rx
from app.states.sensors_management_state import SensorsManagementState


def sensor_form_modal() -> rx.Component:
    return rx.cond(
        SensorsManagementState.is_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        rx.cond(
                            SensorsManagementState.editing_sensor,
                            "Edit Sensor",
                            "Add New Sensor",
                        ),
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Type",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Temperature", value="temperature"),
                                rx.el.option("Humidity", value="humidity"),
                                rx.el.option("Soil Moisture", value="soil_moisture"),
                                rx.el.option("Light", value="light"),
                                rx.el.option("Other", value="other"),
                                value=SensorsManagementState.form_type,
                                on_change=SensorsManagementState.set_form_type,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Unit",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                placeholder="e.g. °C, %",
                                on_change=SensorsManagementState.set_form_unit,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                                default_value=SensorsManagementState.form_unit,
                            ),
                            class_name="mb-4",
                        ),
                        class_name="grid grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Description",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. Main Greenhouse Sensor",
                            on_change=SensorsManagementState.set_form_description,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            default_value=SensorsManagementState.form_description,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Low Threshold",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                placeholder="Min Value",
                                on_change=SensorsManagementState.set_form_threshold_low,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                                default_value=SensorsManagementState.form_threshold_low,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "High Threshold",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                placeholder="Max Value",
                                on_change=SensorsManagementState.set_form_threshold_high,
                                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                                default_value=SensorsManagementState.form_threshold_high,
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-6",
                    ),
                    rx.cond(
                        SensorsManagementState.form_error != "",
                        rx.el.div(
                            SensorsManagementState.form_error,
                            class_name="text-sm text-red-600 mb-4 bg-red-50 p-2 rounded",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=SensorsManagementState.close_modals,
                            class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                        ),
                        rx.el.button(
                            "Save Sensor",
                            on_click=SensorsManagementState.save_sensor,
                            class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md relative z-50",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
                on_click=SensorsManagementState.close_modals,
            ),
            class_name="fixed inset-0 z-50",
        ),
    )


def delete_sensor_modal() -> rx.Component:
    return rx.cond(
        SensorsManagementState.is_delete_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Delete Sensor",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Are you sure you want to delete this sensor? All historical data for this sensor will be lost.",
                        class_name="text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=SensorsManagementState.close_modals,
                            class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                        ),
                        rx.el.button(
                            "Delete",
                            on_click=SensorsManagementState.delete_sensor,
                            class_name="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="bg-white rounded-xl shadow-2xl p-6 w-full max-w-md relative z-50",
                ),
                class_name="fixed inset-0 flex items-center justify-center z-50",
            ),
            rx.el.div(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
                on_click=SensorsManagementState.close_modals,
            ),
            class_name="fixed inset-0 z-50",
        ),
    )