import os
import sqlite3 as sq
import uuid
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


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

    def register_user(e):
        if (
                not username_input.value
                or not email_input.value
                or not password_input.value
        ):
            status_message.value = "All fields are required"
            status_message.color = ft.Colors.RED
            page.update()
            return

        try:
            conn = sq.connect(DB_PATH)
            cursor = conn.cursor()

            # 1. Validar si ya existe el correo
            cursor.execute("SELECT id FROM users WHERE email = ?", (email_input.value,))
            if cursor.fetchone():
                status_message.value = "Email already registered"
                status_message.color = ft.Colors.RED
                conn.close()
                page.update()
                return

            # 2. Validar si ya existe el nombre de usuario
            cursor.execute(
                "SELECT id FROM users WHERE username = ?", (username_input.value,)
            )
            if cursor.fetchone():
                status_message.value = "Username already exists"
                status_message.color = ft.Colors.RED
                conn.close()
                page.update()
                return

            # 3. Inserción segura con marcadores '?'
            new_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO users (id, email, username, password) VALUES (?, ?, ?, ?)",
                (new_id, email_input.value, username_input.value, password_input.value),
            )

            conn.commit()
            conn.close()

            status_message.value = "User registered successfully!"
            status_message.color = ft.Colors.GREEN
            page.update()

        except Exception as ex:
            status_message.value = "Registration error: {}".format(ex)
            status_message.color = ft.Colors.RED
            page.update()

    return ft.Column(
        [
            ft.Text("Register User", size=24, weight=ft.FontWeight.BOLD),
            username_input,
            email_input,
            password_input,
            ft.ElevatedButton(
                content=ft.Text("Register"), on_click=register_user, width=280
            ),
            status_message,
            ft.TextButton("Back to Login", on_click=lambda _: go_to_login()),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )