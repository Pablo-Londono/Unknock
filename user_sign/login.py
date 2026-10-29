import flet as ft
import requests
from config import  IP_GLOBAL
from user_sign.views_login import get_login_view_layout

SERVER_URL = IP_GLOBAL


def get_login_view(page: ft.Page, go_to_register, on_login_success):
    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
        autofocus=True,
    )
    password_input = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=280
    )
    status_message = ft.Text(value="", color=ft.Colors.RED, size=12)

    def login(e):
        if not email_input.value or not password_input.value:
            status_message.value = "All fields are required"
            page.update()
            return

        try:
            # Petición HTTP POST al servidor con el paquete de credenciales
            response = requests.post(
                SERVER_URL,
                json={"email": email_input.value, "password": password_input.value},
            )
            data = response.json()

            # Si el servidor responde con éxito (verdadero)
            if response.status_code == 200 and data.get("success"):
                user_info = data.get("user")
                on_login_success(user_info)
            else:
                status_message.value = data.get("message", "Invalid email or password")
                page.update()

        except requests.exceptions.ConnectionError:
            status_message.value = "No se pudo conectar con el servidor"
            page.update()
        except Exception as ex:
            status_message.value = f"Error: {ex}"
            page.update()

    return get_login_view_layout(
        email_input,
        password_input,
        status_message,
        login,
        go_to_register,
    )
