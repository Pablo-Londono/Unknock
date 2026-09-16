import json
import os
import sqlite3 as sq
import flet as ft
from config.views_config import get_config_view
from dashboard.views_dashboard import get_dashboard_view
from views_courses import get_course_view
from user_sign.views_login import get_login_view
from user_sign.views_register import get_register_view

# Paleta de colores para el Tema Claro (Verdosos)
PRIMARY_COLOR = ft.Colors.GREEN_700
SECONDARY_COLOR = ft.Colors.GREEN_200
SURFACE_COLOR = ft.Colors.WHITE
TEXT_COLOR = ft.Colors.GREEN_900

# Paleta de colores para el Tema Oscuro (Tonos oscuros con acentos verdes)
DARK_PRIMARY_COLOR = ft.Colors.GREEN_400
DARK_SECONDARY_COLOR = ft.Colors.GREEN_800
DARK_SURFACE_COLOR = ft.Colors.GREY_900
DARK_TEXT_COLOR = ft.Colors.GREEN_100

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "local.json")
# users.db se encuentra dentro del subdirectorio user_sign/
DB_PATH = os.path.join(BASE_DIR, "user_sign", "users.db")


def init_db():
    """Inicializa la base de datos users.db dentro de user_sign/ con los 4 campos"""
    conn = sq.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
                                             id TEXT PRIMARY KEY,
                                             email TEXT,
                                             username TEXT,
                                             password TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_app_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            secondary=SECONDARY_COLOR,
            surface=SURFACE_COLOR,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=TEXT_COLOR),
        ),
    )


def get_app_dark_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=DARK_PRIMARY_COLOR,
            secondary=DARK_SECONDARY_COLOR,
            surface=DARK_SURFACE_COLOR,
        ),
        text_theme=ft.TextTheme(
            body_medium=ft.TextStyle(color=DARK_TEXT_COLOR),
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
        print("Error al escribir local.json: {}".format(e))


def main(page: ft.Page):
    init_db()

    page.title = "CBC APP Test_1"
    page.window.width = 380
    page.window.height = 700
    page.window.resizable = False
    page.window.maximizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Cargar configuración guardada
    config_data = load_config()
    current_user = config_data.get("session")

    saved_theme = config_data.get("theme_mode", "light")
    page.theme_mode = (
        ft.ThemeMode.DARK if saved_theme == "dark" else ft.ThemeMode.LIGHT
    )

    page.theme = get_app_theme()
    page.dark_theme = get_app_dark_theme()

    def toggle_theme_mode(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            new_theme_str = "dark"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            new_theme_str = "light"

        cfg = load_config()
        cfg["theme_mode"] = new_theme_str
        save_config(cfg)
        page.update()

    def show_login_view():
        cfg = load_config()
        cfg["session"] = None
        save_config(cfg)
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
        cfg = load_config()
        cfg["session"] = user_info
        save_config(cfg)
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