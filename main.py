import json
import os
import flet as ft
from dashboard.config.views_config import get_config_view
from dashboard.views_courses import get_course_view
from dashboard.views_dashboard import get_dashboard_view
from user_sign.login import get_login_view
from user_sign.register import get_register_view

# ==========================================
# PALETAS DE COLOR
# ==========================================
# Tema Claro
LIGHT_PRIMARY = ft.Colors.BLUE_700
LIGHT_SECONDARY = ft.Colors.BLUE_200
LIGHT_BACKGROUND = ft.Colors.BLUE_50
LIGHT_SURFACE = ft.Colors.WHITE
LIGHT_TEXT = ft.Colors.BLUE_900

# Tema Oscuro
DARK_PRIMARY = ft.Colors.GREEN_400
DARK_SECONDARY = ft.Colors.GREEN_800
DARK_BACKGROUND = ft.Colors.GREY_900
DARK_SURFACE = ft.Colors.GREY_800
DARK_TEXT = ft.Colors.GREEN_100

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "local.json")


def get_light_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=LIGHT_PRIMARY,
            secondary=LIGHT_SECONDARY,
            surface=LIGHT_SURFACE,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=LIGHT_TEXT),
        ),
    )


def get_dark_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=DARK_PRIMARY,
            secondary=DARK_SECONDARY,
            surface=DARK_SURFACE,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=DARK_TEXT),
        ),
    )


# --- Gestión de Configuración Local (JSON unificado) ---
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


# --- Main ---
def main(page: ft.Page):
    page.title = "CBC APP Test_1"
    page.window.width = 380
    page.window.height = 700
    page.window.resizable = True
    page.window.maximizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Configurar temas
    page.theme = get_light_theme()
    page.dark_theme = get_dark_theme()

    # Cargar la preferencia de tema guardada en local.json
    saved_theme = load_theme_preference()
    page.theme_mode = (
        ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
    )

    current_user = load_session()

    def toggle_theme_mode(is_dark: bool):
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        save_theme_preference("dark" if is_dark else "light")
        page.update()

    # --- RUTAS DE NAVEGACIÓN ---

    def show_login_view():
        save_session(None)
        page.controls.clear()
        page.add(
            get_login_view(
                page,
                go_to_register=show_register_view,
                on_login_success=on_login_success,
            )
        )
        page.update()

    def show_register_view():
        page.controls.clear()
        page.add(get_register_view(page, go_to_login=show_login_view))
        page.update()

    def on_login_success(user_info):
        nonlocal current_user
        current_user = user_info
        save_session(user_info)
        show_dashboard_view()

    def show_dashboard_view():
        page.controls.clear()
        page.add(
            get_dashboard_view(
                page,
                current_user=current_user,
                go_to_config=show_config_view,
                go_to_course=show_course_view,
            )
        )
        page.update()

    def show_config_view():
        page.controls.clear()
        page.add(
            get_config_view(
                page,
                go_to_dashboard=show_dashboard_view,
                on_logout=show_login_view,
                toggle_theme=toggle_theme_mode,
            )
        )
        page.update()

    def show_course_view(course_id="c1"):
        page.controls.clear()
        page.add(
            get_course_view(
                page,
                current_user=current_user,
                go_to_config=show_config_view,
                go_to_dashboard=show_dashboard_view,
                course_id=course_id,
            )
        )
        page.update()

    if current_user:
        show_dashboard_view()
    else:
        show_login_view()


if __name__ == "__main__":
    ft.run(main)