import reflex as rx
from app.components.navbar import navbar
from app.components.status_card import database_status_card
from app.components.data_table import data_table
from app.states.db_state import DatabaseState


def system_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "System Status & Integration",
                        class_name="text-2xl font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            database_status_card(),
                            class_name="w-full md:w-1/3 lg:w-1/4 shrink-0",
                        ),
                        rx.el.div(data_table(), class_name="flex-1 w-full min-w-0"),
                        class_name="flex flex-col md:flex-row gap-8 items-start",
                    ),
                    class_name="container mx-auto px-4 py-8",
                ),
                class_name="pb-20",
            ),
            class_name="min-h-screen bg-gray-50",
        ),
        rx.el.div(on_mount=DatabaseState.on_mount),
        class_name="font-['Inter']",
    )