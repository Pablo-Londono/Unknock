import flet as ft


def get_register_view_layout(
        username_input,
        email_input,
        password_input,
        status_message,
        on_register_click,
        go_to_login,
):
    return ft.Column(
        [
            ft.Text("Register User", size=24, weight=ft.FontWeight.BOLD),
            username_input,
            email_input,
            password_input,
            ft.Button(
                content=ft.Text("Register"), on_click=on_register_click, width=280
            ),
            status_message,
            ft.TextButton("Back to Login", on_click=lambda _: go_to_login()),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )