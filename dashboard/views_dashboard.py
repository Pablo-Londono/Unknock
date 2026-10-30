import flet as ft
from dashboard.views_header import get_top_header


def get_dashboard_view(page: ft.Page, current_user, go_to_config, go_to_course=None):
    # Detección del tema actual
    is_dark = page.theme_mode == ft.ThemeMode.DARK
    
    # Colores dinámicos según el modo
    primary_color = ft.Colors.GREEN_400 if is_dark else ft.Colors.BLUE_700
    title_color = ft.Colors.GREEN_100 if is_dark else ft.Colors.BLUE_900

    # 1. Obtener la barra superior unificada
    header_container = get_top_header(page, current_user, go_to_config)

    # 2. Lista de cursos disponibles
    courses_data = [
        {"id": "c1", "title": "Curso 1: Introducción a la Fisica"},
        {"id": "c2", "title": "Curso 2: Introduccion a la Economia"}
    ]

    course_items = []
    for course in courses_data:
        course_id = course["id"]
        course_title = course["title"]

        card = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        # El icono ahora toma el color primario dinámico (verde en oscuro, azul en claro)
                        ft.Icon(ft.Icons.BOOKMARK_BORDER, color=primary_color),
                        ft.Text(
                            course_title,
                            size=12,
                            weight=ft.FontWeight.W_500,
                            expand=True
                        ),
                        ft.Button(
                            content=ft.Text("Ver más", size=11),
                            on_click=lambda _, c_id=course_id: go_to_course(c_id) if go_to_course else None
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10
            )
        )
        course_items.append(card)

    # Columna con desplazamiento (Scroll) para los cursos
    courses_scroll_list = ft.Column(
        controls=course_items,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=10
    )

    return ft.Column(
        [
            header_container,
            ft.Divider(height=10, thickness=1),
            ft.Text("Mis Cursos", size=14, weight=ft.FontWeight.BOLD, color=title_color),
            courses_scroll_list,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        expand=True,
    )
