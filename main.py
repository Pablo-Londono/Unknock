import json
import os
import flet as ft
import requests
from config import IP_GLOBAL
from dashboard.config.views_config import get_config_view
from dashboard.views_courses import get_course_view
from dashboard.views_dashboard import get_dashboard_view
from user_sign.login import get_login_view
from user_sign.register import get_register_view

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "local.json")

# ==========================================
# PALETAS DE COLOR PERSONALIZADAS
# ==========================================
# Tema Claro: Blanco y Azul
LIGHT_PRIMARY = ft.Colors.BLUE_700
LIGHT_SECONDARY = ft.Colors.BLUE_200
LIGHT_SURFACE = ft.Colors.WHITE
LIGHT_TEXT = ft.Colors.BLUE_900

# Tema Oscuro: Verde y Negro
DARK_PRIMARY = ft.Colors.GREEN_400
DARK_SECONDARY = ft.Colors.GREEN_800
DARK_SURFACE = ft.Colors.GREY_900
DARK_TEXT = ft.Colors.GREEN_100

def get_light_theme():
    return ft.Theme(
        font_family="Syne",
        color_scheme=ft.ColorScheme(
            primary=LIGHT_PRIMARY,
            secondary=LIGHT_SECONDARY,
            surface=LIGHT_SURFACE,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=LIGHT_TEXT, font_family="Syne", size=16),
            headline_large=ft.TextStyle(font_family="SyneBold", weight=ft.FontWeight.BOLD, size=26),
            title_medium=ft.TextStyle(font_family="SyneBold", weight=ft.FontWeight.BOLD, size=18),
        ),
    )

def get_dark_theme():
    return ft.Theme(
        font_family="Syne",
        color_scheme=ft.ColorScheme(
            primary=DARK_PRIMARY,
            secondary=DARK_SECONDARY,
            surface=DARK_SURFACE,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=DARK_TEXT, font_family="Syne", size=16),
            headline_large=ft.TextStyle(font_family="SyneBold", weight=ft.FontWeight.BOLD, size=26),
            title_medium=ft.TextStyle(font_family="SyneBold", weight=ft.FontWeight.BOLD, size=18),
        ),
    )


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}


def save_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error al escribir en local.json: {e}")


def load_session():
    config = load_config()
    return config.get("session")


def save_session(user_info):
    config = load_config()
    config["session"] = user_info
    save_config(config)


def load_theme_preference():
    config = load_config()
    return config.get("theme_mode", "light")


def save_theme_preference(mode_str):
    config = load_config()
    config["theme_mode"] = mode_str
    save_config(config)


def validate_session_with_server():
    """Valida automáticamente con el servidor si el ID y el correo de la sesión coinciden en la BD."""
    session = load_session()

    if not session or not isinstance(session, dict):
        return None

    user_id = session.get("id")
    email = session.get("email")

    if not user_id or not email:
        return None

    try:
        url = f"{IP_GLOBAL}/verify"
        response = requests.post(
            url,
            json={"id": user_id, "email": email},
            timeout=4
        )
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            return data.get("user")
    except Exception as e:
        print(f"No se pudo conectar con el servidor para validar la sesión: {e}")

    return None


# --- Main ---
def main(page: ft.Page):
    page.title = "CBC APP Test_1"
    page.window.width = 380
    page.window.height = 700
    page.window.resizable = True
    page.window.maximizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # 1. Registrar las fuentes personalizadas desde la carpeta assets (resources)
    page.fonts = {
        "Syne": "font/syne/static/Syne-Regular.ttf",
        "SyneBold": "font/syne/static/Syne-Bold.ttf",
    }

    # Configurar temas
    page.theme = get_light_theme()
    page.dark_theme = get_dark_theme()

    saved_theme = load_theme_preference()
    page.theme_mode = (
        ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
    )

    # Validamos estrictamente la sesión con el servidor al iniciar
    current_user = validate_session_with_server()

    def toggle_theme_mode(is_dark: bool):
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        save_theme_preference("dark" if is_dark else "light")
        page.update()

    # --- RUTAS DE NAVEGACIÓN USANDO ft.View ---
    def show_login_view():
        save_session(None)
        page.views.clear()

        login_content = get_login_view(
            page,
            go_to_register=lambda _: show_register_view(),
            on_login_success=on_login_success,
        )

        view = login_content if isinstance(login_content, ft.View) else ft.View(
            route="/login",
            controls=[login_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(view)
        page.update()

    def show_register_view(e=None):
        page.views.clear()

        register_content = get_register_view(
            page,
            go_to_login=lambda _: show_login_view()
        )

        view = register_content if isinstance(register_content, ft.View) else ft.View(
            route="/register",
            controls=[register_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(view)
        page.update()

    def on_login_success(user_info):
        nonlocal current_user
        current_user = user_info
        save_session(user_info)
        show_dashboard_view()

    def show_dashboard_view(e=None):
        page.views.clear()

        dashboard_content = get_dashboard_view(
            page,
            current_user=current_user,
            go_to_config=show_config_view,
            go_to_course=show_course_view,
        )

        view = dashboard_content if isinstance(dashboard_content, ft.View) else ft.View(
            route="/dashboard",
            controls=[dashboard_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(view)
        page.update()

    def show_config_view(e=None):
        page.views.clear()

        config_content = get_config_view(
            page,
            go_to_dashboard=show_dashboard_view,
            on_logout=show_login_view,
            toggle_theme=toggle_theme_mode,
        )

        view = config_content if isinstance(config_content, ft.View) else ft.View(
            route="/config",
            controls=[config_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(view)
        page.update()

    def show_course_view(course_id="c1"):
        page.views.clear()

        course_content = get_course_view(
            page,
            current_user=current_user,
            go_to_config=show_config_view,
            go_to_dashboard=show_dashboard_view,
            course_id=course_id,
        )

        view = course_content if isinstance(course_content, ft.View) else ft.View(
            route="/course",
            controls=[course_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(view)
        page.update()

    if current_user:
        show_dashboard_view()
    else:
        save_session(None)
        show_login_view()


if __name__ == "__main__":
    ft.run(main, assets_dir="resources")