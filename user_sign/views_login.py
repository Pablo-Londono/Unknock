import json
import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "user.json")


def get_login_view(page: ft.Page, go_to_register, on_login_success):
    # Campo para Email con KeyboardType.EMAIL
    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
        autofocus=True,
    )
    password_input = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=280
    )
    status_message = ft.Text(value="", color="red", size=12)

    def validate_login(e):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                user_list = raw_data.get("users", [])
        except (FileNotFoundError, json.JSONDecodeError):
            status_message.value = "Error: Unable to read user.json"
            page.update()
            return

        # Validación buscando por la clave 'email'
        found_user = next(
            (
                u
                for u in user_list
                if u.get("email") == email_input.value
                   and u["password"] == password_input.value
            ),
            None,
        )

        if found_user:
            on_login_success(found_user)
        else:
            status_message.value = "Invalid email or password"
            page.update()

    return ft.Column(
        [
            ft.Text("Sign In", size=24, weight="bold"),
            email_input,
            password_input,
            ft.Button(
                content=ft.Text("Login"), on_click=validate_login, width=280
            ),
            status_message,
            ft.TextButton(
                "Don't have an account? Register here",
                on_click=lambda _: go_to_register(),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )