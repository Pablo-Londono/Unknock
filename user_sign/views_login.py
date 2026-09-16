import os
import sqlite3 as sq
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")


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

    def validate_login(e):
        if not email_input.value or not password_input.value:
            status_message.value = "All fields are required"
            page.update()
            return

        try:
            conn = sq.connect(DB_PATH)
            cursor = conn.cursor()

            # Consulta segura con marcadores '?'
            cursor.execute(
                "SELECT id, email, username, password FROM users WHERE email = ? AND password = ?",
                (email_input.value, password_input.value),
            )
            found_user_row = cursor.fetchone()
            conn.close()

            if found_user_row:
                user_info = {
                    "id": found_user_row[0],
                    "email": found_user_row[1],
                    "user": found_user_row[2],
                }
                on_login_success(user_info)
            else:
                status_message.value = "Invalid email or password"
                page.update()

        except Exception as ex:
            status_message.value = "Database error: {}".format(ex)
            page.update()

    return ft.Column(
        [
            ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD),
            email_input,
            password_input,
            ft.ElevatedButton(
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
        expand=True,
    )