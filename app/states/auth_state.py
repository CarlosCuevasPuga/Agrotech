import reflex as rx
import logging
from app.backend.database import DatabaseManager
from app.models.data_models import User

logger = logging.getLogger(__name__)


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    logged_in_user: User | None = None
    login_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_user is not None

    @rx.var
    def user_role(self) -> str:
        return self.logged_in_user["role"] if self.logged_in_user else ""

    @rx.event
    def login(self):
        self.login_error = ""
        if not self.username or not self.password:
            self.login_error = "Please enter both username and password."
            return
        user_data = DatabaseManager.get_user_by_username(self.username)
        if user_data and DatabaseManager.verify_password(
            user_data["password_hash"], self.password
        ):
            self.logged_in_user = user_data
            self.username = ""
            self.password = ""
            return rx.redirect("/")
        else:
            self.login_error = "Invalid username or password."

    @rx.event
    def logout(self):
        self.logged_in_user = None
        return rx.redirect("/login")

    @rx.event
    def on_mount(self):
        current_path = self.router.page.path
        if current_path != "/login" and (not self.is_authenticated):
            return rx.redirect("/login")