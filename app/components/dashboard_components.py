import reflex as rx
from app.states.sensors_state import SensorsState
from app.models.data_models import EnrichedParcel, EnrichedSensor


def status_dot(color: str) -> rx.Component:
    return rx.el.div(
        class_name=rx.match(
            color,
            (
                "green",
                "w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-emerald-200 shadow-sm",
            ),
            (
                "yellow",
                "w-2.5 h-2.5 rounded-full bg-amber-500 shadow-amber-200 shadow-sm animate-pulse",
            ),
            (
                "red",
                "w-2.5 h-2.5 rounded-full bg-red-500 shadow-red-200 shadow-sm animate-pulse",
            ),
            "w-2.5 h-2.5 rounded-full bg-gray-300",
        )
    )


def sensor_sparkline(data: list[dict], color: str) -> rx.Component:
    stroke_color = rx.match(
        color,
        ("green", "#10b981"),
        ("yellow", "#f59e0b"),
        ("red", "#ef4444"),
        "#9ca3af",
    )
    return rx.recharts.line_chart(
        rx.recharts.line(
            data_key="value",
            stroke=stroke_color,
            dot=False,
            stroke_width=2,
            type_="monotone",
        ),
        data=data,
        width="100%",
        height=40,
    )


def sensor_card(sensor: EnrichedSensor) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    sensor["type"].upper(),
                    class_name="text-[10px] font-bold tracking-wider text-gray-500 uppercase",
                ),
                status_dot(sensor["status_color"]),
                class_name="flex justify-between items-center mb-1",
            ),
            rx.el.div(
                rx.cond(
                    sensor["current_value"] != None,
                    rx.el.span(
                        f"{sensor['current_value']}",
                        rx.el.span(
                            sensor["unit"],
                            class_name="text-sm text-gray-400 ml-1 font-normal",
                        ),
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.span("--", class_name="text-2xl font-bold text-gray-300"),
                ),
                class_name="mb-2",
            ),
            rx.el.div(
                sensor_sparkline(sensor["history"], sensor["status_color"]),
                class_name="h-10 w-full opacity-80",
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def parcel_section(parcel: EnrichedParcel) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(parcel["name"], class_name="text-lg font-semibold text-gray-800"),
            rx.el.span(
                parcel["location"],
                class_name="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded-md",
            ),
            class_name="flex items-center gap-3 mb-4",
        ),
        rx.el.div(
            rx.foreach(parcel["sensors"], sensor_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4",
        ),
        class_name="mb-8 bg-gray-50/50 p-6 rounded-2xl border border-gray-200/50",
    )


def alert_item(alert: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "flag_triangle_right", class_name="w-5 h-5 text-amber-600 shrink-0"
            ),
            rx.el.div(
                rx.el.p(
                    alert["type"],
                    class_name="text-xs font-bold text-amber-700 uppercase",
                ),
                rx.el.p(
                    alert["message"], class_name="text-sm text-gray-700 font-medium"
                ),
                rx.el.p(alert["timestamp"], class_name="text-xs text-gray-400 mt-1"),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("check", class_name="w-4 h-4"),
                on_click=lambda: SensorsState.acknowledge_alert(alert["id"]),
                class_name="p-1.5 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors",
                title="Acknowledge",
            ),
            class_name="flex gap-3 items-start",
        ),
        class_name="p-3 bg-amber-50 border-l-4 border-amber-400 rounded-r-lg mb-2",
    )


def alerts_panel() -> rx.Component:
    return rx.cond(
        SensorsState.active_alerts.length() > 0,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Active Alerts",
                    class_name="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3",
                ),
                rx.el.span(
                    SensorsState.active_alerts.length(),
                    class_name="bg-red-100 text-red-600 text-xs font-bold px-2 py-0.5 rounded-full",
                ),
                class_name="flex justify-between items-center",
            ),
            rx.el.div(
                rx.foreach(SensorsState.active_alerts, alert_item),
                class_name="max-h-[300px] overflow-y-auto pr-2 scrollbar-thin",
            ),
            class_name="bg-white rounded-xl border border-gray-200 p-4 shadow-sm h-fit sticky top-4",
        ),
    )