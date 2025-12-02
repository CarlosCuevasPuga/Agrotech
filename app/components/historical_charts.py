import reflex as rx
from app.states.analytics_state import AnalyticsState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.5rem",
        "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
        "fontSize": "0.875rem",
        "padding": "0.5rem",
    },
    "item_style": {"color": "#374151", "fontWeight": "500"},
    "separator": "",
}


def historical_line_chart() -> rx.Component:
    return rx.el.div(
        rx.recharts.responsive_container(
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, stroke="#E5E7EB"
                ),
                rx.recharts.x_axis(
                    data_key="timestamp",
                    stroke="#9CA3AF",
                    font_size=12,
                    tick_line=False,
                    axis_line=False,
                    min_tick_gap=30,
                ),
                rx.recharts.y_axis(
                    stroke="#9CA3AF",
                    font_size=12,
                    tick_line=False,
                    axis_line=False,
                    domain=["auto", "auto"],
                ),
                rx.recharts.tooltip(**TOOLTIP_PROPS),
                rx.recharts.area(
                    type_="monotone",
                    data_key="value",
                    stroke="#4F46E5",
                    fill="#EEF2FF",
                    stroke_width=2,
                    active_dot={"r": 6, "strokeWidth": 0},
                ),
                data=AnalyticsState.chart_data,
            ),
            width="100%",
            height=400,
        ),
        class_name="w-full h-[400px] bg-white rounded-xl border border-gray-200 p-4 shadow-sm [&_.recharts-tooltip-item-name]:hidden",
    )