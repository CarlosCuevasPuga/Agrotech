import reflex as rx
from app.states.db_state import DatabaseState


def status_indicator(
    label: str,
    active: bool,
    active_color: str = "bg-emerald-500",
    inactive_color: str = "bg-red-500",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                active,
                f"w-3 h-3 rounded-full {active_color} animate-pulse",
                f"w-3 h-3 rounded-full {inactive_color}",
            )
        ),
        rx.el.span(label, class_name="text-sm font-medium text-gray-600"),
        class_name="flex items-center gap-3 p-2 rounded-lg bg-gray-50 border border-gray-100",
    )


def console_log_item(log: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(">", class_name="text-indigo-400 mr-2 font-bold"),
        log,
        class_name="text-xs font-mono text-gray-300 py-1 border-b border-gray-700/50 last:border-0",
    )


def database_status_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("database", class_name="w-6 h-6 text-indigo-600"),
                rx.el.h2(
                    "Database Status", class_name="text-xl font-bold text-gray-900"
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.button(
                rx.cond(
                    DatabaseState.is_loading,
                    rx.icon("loader", class_name="w-4 h-4 animate-spin"),
                    rx.icon("refresh-cw", class_name="w-4 h-4"),
                ),
                on_click=DatabaseState.check_connection,
                disabled=DatabaseState.is_loading,
                class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            status_indicator("Connection", DatabaseState.status["connected"]),
            status_indicator("Schema Ready", DatabaseState.status["table_exists"]),
            rx.el.div(
                rx.el.span(
                    "Records",
                    class_name="text-xs text-gray-400 uppercase font-bold tracking-wider",
                ),
                rx.el.span(
                    DatabaseState.status["record_count"],
                    class_name="text-2xl font-bold text-indigo-600",
                ),
                class_name="flex flex-col justify-center items-center p-3 bg-indigo-50/50 rounded-xl border border-indigo-100",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Initialization",
                    class_name="text-sm font-semibold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Create or repair the database schema for MAIoTALib data.",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                rx.el.button(
                    rx.cond(
                        DatabaseState.is_loading,
                        "Processing...",
                        "Initialize System Schema",
                    ),
                    on_click=DatabaseState.initialize_database,
                    disabled=DatabaseState.is_loading,
                    class_name=rx.cond(
                        DatabaseState.is_loading,
                        "w-full py-2.5 px-4 bg-gray-100 text-gray-400 rounded-xl font-medium cursor-not-allowed",
                        "w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-medium transition-all shadow-lg shadow-indigo-200 active:scale-95",
                    ),
                ),
            ),
            class_name="bg-white rounded-xl border border-gray-200 p-5 shadow-sm mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Data Import", class_name="text-sm font-semibold text-gray-900 mb-2"
                ),
                rx.el.p(
                    "Import new records from MAIoTALib.py source file.",
                    class_name="text-sm text-gray-500 mb-4",
                ),
                rx.el.button(
                    rx.cond(
                        DatabaseState.is_loading,
                        rx.el.span(
                            "Importing...",
                            class_name="flex items-center justify-center gap-2",
                        ),
                        rx.el.span(
                            rx.icon("file-down", class_name="w-4 h-4 mr-2"),
                            "Import Data from File",
                            class_name="flex items-center justify-center",
                        ),
                    ),
                    on_click=DatabaseState.import_maiota_data,
                    disabled=DatabaseState.is_loading,
                    class_name=rx.cond(
                        DatabaseState.is_loading,
                        "w-full py-2.5 px-4 bg-gray-100 text-gray-400 rounded-xl font-medium cursor-not-allowed",
                        "w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-medium transition-all shadow-lg shadow-emerald-200 active:scale-95",
                    ),
                ),
            ),
            class_name="bg-white rounded-xl border border-gray-200 p-5 shadow-sm mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "System Logs",
                    class_name="text-xs font-semibold text-gray-400 uppercase",
                ),
                class_name="flex justify-between items-center mb-2 px-1",
            ),
            rx.el.div(
                rx.foreach(DatabaseState.logs, console_log_item),
                class_name="bg-gray-900 rounded-xl p-4 h-48 overflow-y-auto shadow-inner scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent",
            ),
            class_name="mt-auto",
        ),
        class_name="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 w-full max-w-md mx-auto",
    )