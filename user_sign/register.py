import re
import flet as ft
import requests
from config import IP_GLOBAL
from user_sign.views_register import get_register_view_layout

SERVER_URL = IP_GLOBAL


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def get_register_view(page: ft.Page, go_to_login):
    username_input = ft.TextField(label="Full Name / Username", width=280)
    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
    )
    password_input = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=280
    )
    status_message = ft.Text(value="", color=ft.Colors.RED, size=12)

    def register(e):
        if (
                not username_input.value
                or not email_input.value
                or not password_input.value
        ):
            status_message.value = "All fields are required"
            status_message.color = ft.Colors.RED
            page.update()
            return

        if not is_valid_email(email_input.value):
            status_message.value = "Invalid email format"
            status_message.color = ft.Colors.RED
            page.update()
            return

        try:
            # Petición HTTP POST enviando los datos de registro al servidor
            response = requests.post(
                SERVER_URL,
                json={
                    "username": username_input.value,
                    "email": email_input.value,
                    "password": password_input.value,
                },
            )
            data = response.json()

            if response.status_code == 200 and data.get("success"):
                status_message.value = "User registered successfully!"
                status_message.color = ft.Colors.GREEN
                page.update()
            else:
                status_message.value = data.get("message", "Registration error")
                status_message.color = ft.Colors.RED
                page.update()

        except requests.exceptions.ConnectionError:
            status_message.value = "No se pudo conectar con el servidor"
            status_message.color = ft.Colors.RED
            page.update()
        except Exception as ex:
            status_message.value = f"Error: {ex}"
            status_message.color = ft.Colors.RED
            page.update()

    return get_register_view_layout(
        username_input,
        email_input,
        password_input,
        status_message,
        register,
        go_to_login,
    )