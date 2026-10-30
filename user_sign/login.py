import flet as ft
import requests
from config import IP_GLOBAL
from components.loading_overlay import LoadingOverlay

def get_login_view(page: ft.Page, go_to_register, on_login_success):
    # Instanciamos el overlay pasándole la página
    loading_overlay = LoadingOverlay(page)

    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
        autofocus=True,
    )
    password_input = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=280
    )
    status_message = ft.Text(value="", color=ft.Colors.RED, size=12)

    def login(e):
        if not email_input.value or not password_input.value:
            status_message.value = "All fields are required"
            status_message.color = ft.Colors.RED
            page.update()
            return

        # ==========================================
        # AQUÍ SE MUESTRA EL OVERLAY DE CARGA
        # ==========================================
        loading_overlay.show("Connecting to server...")
        status_message.value = ""

        async def background_login():
            try:
                url = f"{IP_GLOBAL}/login"
                response = requests.post(
                    url,
                    json={"email": email_input.value, "password": password_input.value},
                    timeout=5
                )
                data = response.json()

                # ==========================================
                # OCULTAMOS EL OVERLAY AL RECIBIR RESPUESTA
                # ==========================================
                loading_overlay.hide()

                if response.status_code == 200 and data.get("success"):
                    user_info = data.get("user")
                    status_message.value = "Login successful!"
                    status_message.color = ft.Colors.GREEN
                    page.update()
                    on_login_success(user_info)
                else:
                    status_message.value = data.get("message", "Invalid email or password")
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

        page.run_task(background_login)

    login_button = ft.Button(
        content="Login",
        on_click=login,
        width=280
    )

    register_button = ft.TextButton(
        content=ft.Text("Don't have an account? Register here"),
        on_click=go_to_register,
    )

    # Color de título dinámico según el modo de tema de la página
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    title_color = ft.Colors.GREEN_400 if is_dark else ft.Colors.BLUE_900

    return ft.View(
        route="/login",
        controls=[
            ft.Column(
                [
                    ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD, color=title_color),
                    email_input,
                    password_input,
                    login_button,
                    status_message,
                    register_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )