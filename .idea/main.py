import json
import os
import flet as ft
from dashboard.config.views_config import get_config_view
from dashboard.views_dashboard import get_dashboard_view
from user_sign.views_login import get_login_view
from user_sign.views_register import get_register_view


# PALETA CLARA ORIGINAL (Verde Esmeralda)
LIGHT_PRIMARY = ft.Colors.GREEN_700  # Verde esmeralda principal
LIGHT_SECONDARY = ft.Colors.GREEN_200  # Verde suave para acentos
LIGHT_SURFACE = ft.Colors.WHITE  # Blanco para tarjetas
LIGHT_TEXT = ft.Colors.GREEN_900  # Verde oscuro para texto

# PALETA OSCURA (Verde Menta Nocturno)
DARK_PRIMARY = ft.Colors.GREEN_400  # Verde brillante para elementos activos
DARK_SECONDARY = ft.Colors.GREEN_800  # Verde bosque oscuro para bordes y acentos
DARK_SURFACE = ft.Colors.GREY_900  # Tarjetas y fondos oscuros
DARK_TEXT = ft.Colors.GREEN_100  # Texto verde claro legible

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "local.json")


def get_app_theme():
    """Retorna el tema Claro original en tonos verdes"""
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


def get_app_dark_theme():
    """Retorna el tema Oscuro en tonos verdes nocturnos"""
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


# --- Gestión de Sesión y Configuración Local ---
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
        print(f"Error escribiendo en local.json: {e}")
        try:
            with open(CONFIG_PATH, "w+", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as retry_error:
            print(f"No se pudo crear local.json: {retry_error}")


def load_session():
    config = load_config()
    return config.get("session")


def save_session(user_info):
    config = load_config()
    config["session"] = user_info
    save_config(config)


def save_theme_preference(mode_str):
    config = load_config()
    config["theme_mode"] = mode_str
    save_config(config)


def load_theme_preference():
    config = load_config()
    return config.get("theme_mode", "light")


# --- Main ---
def main(page: ft.Page):
    page.title = "CBC APP Test_1"
    page.window.width = 380
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Inyección de temas verde claro y verde oscuro
    page.theme = get_app_theme()
    page.dark_theme = get_app_dark_theme()

    # Recuperación de estado guardado en local.json
    saved_theme = load_theme_preference()
    page.theme_mode = (
        ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
    )
    page.bgcolor = None  # Transición dinámica entre fondos

    current_user = load_session()

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
                on_theme_changed=save_theme_preference,
            )
        )
        page.update()

    if current_user:
        show_dashboard_view()
    else:
        show_login_view()


if __name__ == "__main__":
    ft.run(main)