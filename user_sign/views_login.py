import flet as ft


def get_login_view_layout(
        email_input, password_input, status_message, on_login_click, go_to_register
):
    return ft.Column(
        [
            ft.Text("Sign In", size=24, weight=ft.FontWeight.BOLD),
            email_input,
            password_input,
            ft.Button(
                content=ft.Text("Login"), on_click=on_login_click, width=280
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