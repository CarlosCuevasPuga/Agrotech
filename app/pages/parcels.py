import reflex as rx
from app.components.navbar import navbar
from app.states.parcels_state import ParcelsState
from app.components.parcel_forms import parcel_form_modal, delete_parcel_modal
from app.models.data_models import Parcel


def parcel_row(parcel: Parcel) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("map-pin", class_name="w-4 h-4 text-blue-500 mr-3"),
                rx.el.span(parcel["name"], class_name="font-medium text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            parcel["location"], class_name="px-6 py-4 whitespace-nowrap text-gray-500"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.a(
                    rx.icon("settings-2", class_name="w-4 h-4 mr-1"),
                    "Sensors",
                    href=f"/parcels/{parcel['id']}/sensors",
                    class_name="inline-flex items-center px-3 py-1.5 bg-blue-50 text-blue-600 hover:bg-blue-100 rounded-lg text-sm font-medium transition-colors mr-2",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: ParcelsState.open_edit_modal(parcel),
                    class_name="p-2 text-gray-500 hover:bg-gray-100 hover:text-blue-600 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: ParcelsState.open_delete_modal(parcel),
                    class_name="p-2 text-gray-500 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="bg-white hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors",
    )


def parcels_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Parcel Management",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-4 h-4 mr-2"),
                        "Add Parcel",
                        on_click=ParcelsState.open_add_modal,
                        class_name="flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors shadow-sm font-medium",
                    ),
                    class_name="flex justify-between items-center mb-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Search parcels...",
                            on_change=ParcelsState.set_search_query,
                            class_name="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                        ),
                        class_name="relative max-w-md mb-6",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Name",
                                        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Location",
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
                                rx.foreach(ParcelsState.filtered_parcels, parcel_row)
                            ),
                            class_name="min-w-full",
                        ),
                        rx.cond(
                            ParcelsState.filtered_parcels.length() == 0,
                            rx.el.div(
                                rx.icon(
                                    "map",
                                    class_name="w-12 h-12 text-gray-300 mb-3 mx-auto",
                                ),
                                rx.el.p(
                                    "No parcels found",
                                    class_name="text-gray-500 font-medium text-center",
                                ),
                                class_name="py-12 flex flex-col items-center justify-center",
                            ),
                        ),
                        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="container mx-auto px-4 py-8 max-w-6xl",
            ),
            class_name="min-h-screen bg-gray-50 pb-20",
        ),
        parcel_form_modal(),
        delete_parcel_modal(),
        rx.el.div(on_mount=ParcelsState.load_parcels),
        class_name="font-['Inter']",
    )