import reflex as rx
from app.components.navbar import navbar
from app.states.alerts_state import AlertsState
from app.models.data_models import EnrichedAlert


def alert_status_badge(acknowledged: bool) -> rx.Component:
    return rx.cond(
        acknowledged,
        rx.el.span(
            "Acknowledged",
            class_name="bg-gray-100 text-gray-600 text-xs font-medium px-2.5 py-0.5 rounded-full border border-gray-200",
        ),
        rx.el.span(
            "New / Pending",
            class_name="bg-red-100 text-red-600 text-xs font-bold px-2.5 py-0.5 rounded-full border border-red-200 animate-pulse",
        ),
    )


def alert_row(alert: EnrichedAlert) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("bell", class_name="w-4 h-4 text-gray-400 mr-3"),
                rx.el.span(
                    alert["timestamp"].replace("T", " ")[:19],
                    class_name="font-mono text-xs text-gray-500",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    alert["sensor_desc"], class_name="text-sm font-medium text-gray-900"
                ),
                rx.el.p(alert["parcel_name"], class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                alert["type"],
                class_name="uppercase text-xs font-bold tracking-wider "
                + rx.cond(
                    alert["type"].contains("HIGH"), "text-red-600", "text-amber-600"
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(alert["message"], class_name="text-sm text-gray-700"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            alert_status_badge(alert["acknowledged"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.cond(
                ~alert["acknowledged"],
                rx.el.button(
                    rx.icon("check", class_name="w-4 h-4 mr-1"),
                    "Ack",
                    on_click=lambda: AlertsState.acknowledge_alert(alert["id"]),
                    class_name="flex items-center px-3 py-1.5 bg-emerald-50 text-emerald-600 hover:bg-emerald-100 rounded-lg text-xs font-bold transition-colors border border-emerald-200",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right",
        ),
        class_name="bg-white hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors",
    )


def alerts_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.el.option("All Sensors", value="0"),
                rx.foreach(
                    AlertsState.sensors,
                    lambda s: rx.el.option(s["description"], value=s["id"]),
                ),
                on_change=AlertsState.set_filter_sensor,
                class_name="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500",
            ),
            rx.el.select(
                rx.el.option("All Types", value="all"),
                rx.el.option("High Threshold", value="THRESHOLD_HIGH"),
                rx.el.option("Low Threshold", value="THRESHOLD_LOW"),
                on_change=AlertsState.set_filter_type,
                class_name="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500",
            ),
            rx.el.select(
                rx.el.option("Unacknowledged", value="unacknowledged"),
                rx.el.option("Acknowledged", value="acknowledged"),
                rx.el.option("All Status", value="all"),
                on_change=AlertsState.set_filter_acknowledged,
                class_name="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500",
            ),
            class_name="flex flex-wrap gap-3",
        ),
        rx.el.div(
            rx.el.span("Pending: ", class_name="text-gray-500 text-sm"),
            rx.el.span(
                AlertsState.pending_alerts,
                class_name="text-red-600 font-bold text-lg ml-1",
            ),
            class_name="flex items-center bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm",
        ),
        class_name="flex flex-col md:flex-row justify-between items-center gap-4 mb-6",
    )


def alerts_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "System Alerts", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Monitor and manage sensor threshold violations.",
                        class_name="text-gray-500",
                    ),
                    class_name="mb-6",
                ),
                alerts_filters(),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Time",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Source",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Type",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Message",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Status",
                                    class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "Action",
                                    class_name="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider",
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(rx.foreach(AlertsState.alerts, alert_row)),
                        class_name="min-w-full",
                    ),
                    rx.cond(
                        AlertsState.alerts.length() == 0,
                        rx.el.div(
                            rx.icon(
                                "check_check",
                                class_name="w-12 h-12 text-green-300 mb-3 mx-auto",
                            ),
                            rx.el.p(
                                "No alerts found",
                                class_name="text-gray-500 font-medium text-center",
                            ),
                            class_name="py-12 flex flex-col items-center justify-center",
                        ),
                    ),
                    class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
                ),
                class_name="container mx-auto px-4 py-8 max-w-6xl",
            ),
            class_name="min-h-screen bg-gray-50 pb-20",
        ),
        rx.el.div(on_mount=AlertsState.load_initial_data),
        class_name="font-['Inter']",
    )