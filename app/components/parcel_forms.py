import reflex as rx
from app.states.parcels_state import ParcelsState


def parcel_form_modal() -> rx.Component:
    return rx.cond(
        ParcelsState.is_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        rx.cond(
                            ParcelsState.editing_parcel, "Edit Parcel", "Add New Parcel"
                        ),
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Name",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. North Field",
                            on_change=ParcelsState.set_form_name,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            default_value=ParcelsState.form_name,
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Location",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            placeholder="e.g. Sector A-1",
                            on_change=ParcelsState.set_form_location,
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                            default_value=ParcelsState.form_location,
                        ),
                        class_name="mb-4",
                    ),
                    rx.cond(
                        ParcelsState.form_error != "",
                        rx.el.div(
                            ParcelsState.form_error,
                            class_name="text-sm text-red-600 mb-4 bg-red-50 p-2 rounded",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=ParcelsState.close_modals,
                            class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                        ),
                        rx.el.button(
                            "Save Parcel",
                            on_click=ParcelsState.save_parcel,
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
                on_click=ParcelsState.close_modals,
            ),
            class_name="fixed inset-0 z-50",
        ),
    )


def delete_parcel_modal() -> rx.Component:
    return rx.cond(
        ParcelsState.is_delete_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Delete Parcel",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "Are you sure you want to delete this parcel? This action cannot be undone and will delete all associated sensors.",
                        class_name="text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=ParcelsState.close_modals,
                            class_name="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                        ),
                        rx.el.button(
                            "Delete",
                            on_click=ParcelsState.delete_parcel,
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
                on_click=ParcelsState.close_modals,
            ),
            class_name="fixed inset-0 z-50",
        ),
    )