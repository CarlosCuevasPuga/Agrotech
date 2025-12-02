import reflex as rx
from app.states.db_state import DatabaseState
from app.models.data_models import MaiotaRecord


def status_badge(category: str) -> rx.Component:
    return rx.el.span(
        category,
        class_name=rx.match(
            category,
            (
                "SENSOR",
                "bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-blue-200",
            ),
            (
                "ACTUATOR",
                "bg-purple-100 text-purple-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-purple-200",
            ),
            (
                "SYSTEM",
                "bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-gray-200",
            ),
            (
                "NETWORK",
                "bg-emerald-100 text-emerald-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-emerald-200",
            ),
            "bg-orange-100 text-orange-800 text-xs font-medium px-2.5 py-0.5 rounded-full border border-orange-200",
        ),
    )


def table_row(record: MaiotaRecord) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("cpu", class_name="w-4 h-4 text-gray-400 mr-2"),
                rx.el.span(record["source_key"], class_name="font-medium"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
        ),
        rx.el.td(
            status_badge(record["category"]), class_name="px-6 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.span(
                record["value_str"],
                class_name="font-mono text-xs bg-gray-50 px-2 py-1 rounded border border-gray-100",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(
            rx.el.div(
                record["data_type"],
                class_name="text-xs text-gray-500 uppercase tracking-wide",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(record["timestamp"], class_name="text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        class_name="bg-white hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def data_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "System Records", class_name="text-lg font-bold text-gray-900"
                ),
                rx.el.p(
                    "View and filter imported MAIoTALib data.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search records...",
                        on_change=DatabaseState.set_search_query.debounce(300),
                        class_name="pl-9 pr-4 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent w-64 transition-all",
                    ),
                    class_name="relative",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 p-6 border-b border-gray-100",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Source Key",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Category",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Value",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Timestamp",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50/50",
                    )
                ),
                rx.el.tbody(rx.foreach(DatabaseState.records, table_row)),
                class_name="min-w-full",
            ),
            rx.cond(
                DatabaseState.records.length() == 0,
                rx.el.div(
                    rx.icon("inbox", class_name="w-12 h-12 text-gray-300 mb-3 mx-auto"),
                    rx.el.p(
                        "No records found",
                        class_name="text-gray-500 font-medium text-center",
                    ),
                    rx.el.p(
                        "Try adjusting filters or importing data.",
                        class_name="text-sm text-gray-400 text-center",
                    ),
                    class_name="py-12 flex flex-col items-center justify-center",
                ),
            ),
            class_name="overflow-x-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Showing page ", class_name="text-gray-500"),
                rx.el.span(
                    DatabaseState.page, class_name="font-semibold text-gray-900 mx-1"
                ),
                rx.el.span(" of ", class_name="text-gray-500"),
                rx.el.span(
                    DatabaseState.total_pages,
                    class_name="font-semibold text-gray-900 ml-1",
                ),
                class_name="text-sm",
            ),
            rx.el.div(
                rx.el.button(
                    "Previous",
                    on_click=DatabaseState.prev_page,
                    disabled=~DatabaseState.has_prev_page,
                    class_name=rx.cond(
                        DatabaseState.has_prev_page,
                        "px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors",
                        "px-4 py-2 text-sm font-medium text-gray-300 bg-gray-50 border border-gray-200 rounded-lg cursor-not-allowed",
                    ),
                ),
                rx.el.button(
                    "Next",
                    on_click=DatabaseState.next_page,
                    disabled=~DatabaseState.has_next_page,
                    class_name=rx.cond(
                        DatabaseState.has_next_page,
                        "px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors",
                        "px-4 py-2 text-sm font-medium text-gray-300 bg-gray-50 border border-gray-200 rounded-lg cursor-not-allowed",
                    ),
                ),
                class_name="flex gap-2",
            ),
            class_name="flex items-center justify-between p-4 border-t border-gray-100 bg-gray-50/50 rounded-b-xl",
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm w-full",
    )