import re
import flet as ft
import requests
from config import IP_GLOBAL
from components.loading_overlay import LoadingOverlay

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def get_register_view(page: ft.Page, go_to_login):
    loading_overlay = LoadingOverlay(page)

    username_input = ft.TextField(label="Full Name / Username", width=280)
    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
    )
    password_input = ft.TextField(
        label="Password", 
        password=True, 
        can_reveal_password=True, 
        width=280
    )
    status_message = ft.Text(value="", color=ft.Colors.RED, size=12)

    def register(e):
        if not username_input.value or not email_input.value or not password_input.value:
            status_message.value = "All fields are required"
            status_message.color = ft.Colors.RED
            page.update()
            return

        if not is_valid_email(email_input.value):
            status_message.value = "Invalid email format"
            status_message.color = ft.Colors.RED
            page.update()
            return

        loading_overlay.show("Registering user...")
        status_message.value = ""

        async def background_register():
            try:
                url = f"{IP_GLOBAL}/register"
                response = requests.post(
                    url,
                    json={
                        "username": username_input.value,
                        "email": email_input.value,
                        "password": password_input.value,
                    },
                    timeout=5
                )
                data = response.json()

                loading_overlay.hide()

                if response.status_code == 200 and data.get("success"):
                    status_message.value = "User registered successfully!"
                    status_message.color = ft.Colors.GREEN
                    page.update()
                else:
                    status_message.value = data.get("message", "Registration error")
                    status_message.color = ft.Colors.RED
                    page.update()

            except requests.exceptions.ConnectionError:
                loading_overlay.hide()
                status_message.value = "No se pudo conectar con el servidor"
                status_message.color = ft.Colors.RED
                page.update()
            except requests.exceptions.Timeout:
                loading_overlay.hide()
                status_message.value = "El servidor tardó demasiado en responder"
                status_message.color = ft.Colors.RED
                page.update()
            except Exception as ex:
                loading_overlay.hide()
                status_message.value = f"Error: {ex}"
                status_message.color = ft.Colors.RED
                page.update()

        page.run_task(background_register)

    register_button = ft.Button(
        content="Register", 
        on_click=register, 
        width=280
    )

    login_button = ft.TextButton(
        content=ft.Text("Already have an account? Login here"),
        on_click=go_to_login,
    )

    is_dark = page.theme_mode == ft.ThemeMode.DARK
    title_color = ft.Colors.GREEN_400 if is_dark else ft.Colors.BLUE_900

    return ft.View(
        route="/register",
        controls=[
            ft.Column(
                [
                    ft.Text("Create Account", size=24, weight=ft.FontWeight.BOLD, color=title_color),
                    username_input,
                    email_input,
                    password_input,
                    register_button,
                    status_message,
                    login_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

