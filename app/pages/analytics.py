import reflex as rx
from app.components.navbar import navbar
from app.components.historical_charts import historical_line_chart
from app.states.analytics_state import AnalyticsState


def analytics_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Select Sensor",
                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
            ),
            rx.el.select(
                rx.foreach(
                    AnalyticsState.sensors,
                    lambda s: rx.el.option(s["description"], value=s["id"]),
                ),
                value=AnalyticsState.selected_sensor_id,
                on_change=AnalyticsState.set_sensor,
                class_name="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none shadow-sm",
            ),
            class_name="w-full md:w-64",
        ),
        rx.el.div(
            rx.el.label(
                "Start Date",
                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
            ),
            rx.el.input(
                type="date",
                on_change=AnalyticsState.set_start_date,
                class_name="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none shadow-sm",
                default_value=AnalyticsState.start_date,
            ),
            class_name="w-full md:w-40",
        ),
        rx.el.div(
            rx.el.label(
                "End Date",
                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5",
            ),
            rx.el.input(
                type="date",
                on_change=AnalyticsState.set_end_date,
                class_name="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 outline-none shadow-sm",
                default_value=AnalyticsState.end_date,
            ),
            class_name="w-full md:w-40",
        ),
        rx.el.div(
            rx.el.label(
                "Actions",
                class_name="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1.5 opacity-0",
            ),
            rx.el.button(
                rx.cond(
                    AnalyticsState.is_loading,
                    rx.icon("loader", class_name="w-4 h-4 animate-spin"),
                    rx.icon("refresh-cw", class_name="w-4 h-4"),
                ),
                "Refresh",
                on_click=AnalyticsState.load_history,
                disabled=AnalyticsState.is_loading,
                class_name="flex items-center justify-center gap-2 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors shadow-sm h-[38px]",
            ),
            class_name="w-full md:w-auto",
        ),
        class_name="flex flex-col md:flex-row gap-4 p-4 bg-white rounded-xl border border-gray-200 shadow-sm mb-6 items-end",
    )


def analytics_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Historical Analytics",
                    class_name="text-2xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Analyze sensor data trends over time.",
                    class_name="text-gray-500 mb-6",
                ),
                analytics_controls(),
                rx.cond(
                    AnalyticsState.chart_data.length() > 0,
                    historical_line_chart(),
                    rx.el.div(
                        rx.icon(
                            "line-chart", class_name="w-12 h-12 text-gray-300 mb-3"
                        ),
                        rx.el.p(
                            "No data available for selected range.",
                            class_name="text-gray-500 font-medium",
                        ),
                        class_name="w-full h-[400px] bg-white rounded-xl border border-gray-200 flex flex-col items-center justify-center border-dashed",
                    ),
                ),
                class_name="container mx-auto px-4 py-8 max-w-6xl",
            ),
            class_name="min-h-screen bg-gray-50 pb-20",
        ),
        rx.el.div(on_mount=AnalyticsState.load_initial_data),
        class_name="font-['Inter']",
    )