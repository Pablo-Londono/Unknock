import json
import os
import uuid
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "user.json")


def get_register_view(page: ft.Page, go_to_login):
    # Campos de entrada: Nombre, Correo y Contraseña
    username_input = ft.TextField(label="Full Name / Username", width=280)
    email_input = ft.TextField(
        label="Email",
        keyboard_type=ft.KeyboardType.EMAIL,
        width=280,
    )
    password_input = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=280
    )
    status_message = ft.Text(value="", color="red", size=12)

    def register_user(e):
        # Validar que todos los campos estén llenos
        if (
                not username_input.value
                or not email_input.value
                or not password_input.value
        ):
            status_message.value = "All fields are required"
            status_message.color = "red"
            page.update()
            return

        try:
            file_data = {"users": []}
            if os.path.exists(JSON_PATH):
                with open(JSON_PATH, "r", encoding="utf-8") as file:
                    file_data = json.load(file)

            user_list = file_data.get("users", [])

            # Comprobar si el correo ya existe
            if any(u.get("email") == email_input.value for u in user_list):
                status_message.value = "Email already registered"
                status_message.color = "red"
                page.update()
                return

            # Comprobar si el nombre de usuario ya existe
            if any(u.get("user") == username_input.value for u in user_list):
                status_message.value = "Username already exists"
                status_message.color = "red"
                page.update()
                return

            # Crear y agregar nuevo usuario
            new_user = {
                "id": str(uuid.uuid4()),
                "user": username_input.value,
                "email": email_input.value,
                "password": password_input.value,
            }
            user_list.append(new_user)
            file_data["users"] = user_list

            # Guardar datos actualizados en user.json
            with open(JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(file_data, file, indent=4)

            status_message.value = "User registered successfully!"
            status_message.color = "green"
            page.update()

        except Exception as ex:
            status_message.value = f"Registration error: {ex}"
            status_message.color = "red"
            page.update()

    return ft.Column(
        [
            ft.Text("Register User", size=24, weight="bold"),
            username_input,
            email_input,
            password_input,
            ft.Button(
                content=ft.Text("Register"), on_click=register_user, width=280
            ),
            status_message,
            ft.TextButton("Back to Login", on_click=lambda _: go_to_login()),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )