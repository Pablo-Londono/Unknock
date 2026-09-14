import flet as ft
from dashboard.views_header import get_top_header


def get_course_view(page: ft.Page, current_user, go_to_config, go_to_dashboard, course_id=""):
    header = get_top_header(page, current_user, go_to_config)

    back_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK, size=16),
                ft.Text("Volver a mis cursos", size=12),
            ],
            spacing=4,
        ),
        on_click=lambda _: go_to_dashboard(),
    )

    return ft.Column(
        [
            header,
            ft.Divider(height=10, thickness=1),
            ft.Row([back_button], alignment=ft.MainAxisAlignment.START),
            ft.Text(f"Curso ID: {course_id}", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Espacio reservado para el mapa de niveles con islitas.",
                size=12,
                color=ft.Colors.GREY_600,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        expand=True,
    )