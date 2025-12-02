import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Agrotech Login",
                    class_name="text-2xl font-bold text-center text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Username",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="text",
                        placeholder="Enter username",
                        on_change=AuthState.set_username,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors",
                        default_value=AuthState.username,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="Enter password",
                        on_change=AuthState.set_password,
                        class_name="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors",
                        default_value=AuthState.password,
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        AuthState.login_error,
                        class_name="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-md border border-red-100",
                    ),
                ),
                rx.el.button(
                    "Sign In",
                    on_click=AuthState.login,
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors shadow-sm",
                ),
                class_name="bg-white p-8 rounded-xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen bg-gray-50",
        ),
        class_name="min-h-screen w-full font-['Inter']",
    )