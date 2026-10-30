import json
import os
import flet as ft

# Definir la ruta base para encontrar el JSON dentro de tu estructura de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "courses", "sub", "fisica_1.json")

def load_course_config(course_id="c1"):
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(course_id, {})
        except Exception as e:
            print(f"Error al leer el JSON: {e}")
            return {}
    return {}

def get_course_view(page: ft.Page, current_user, go_to_config, go_to_dashboard, course_id="c1"):
    # 1. Cargar los datos del curso desde el JSON
    course_data = load_course_config(course_id)

    course_title = course_data.get("title", "Curso")
    course_description = course_data.get("description", "")
    lessons = course_data.get("lessons", [])

    # Botón de regreso al dashboard principal ("Volver a mis cursos")
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

    # Función para ir a la vista de la lección usando el sistema de vistas nativo de Flet
    def go_to_lesson(lesson_title):
        page.views.clear()

        def return_to_course(_):
            page.views.clear()
            page.views.append(ft.View(
                route="/course",
                controls=[get_course_view(page, current_user, go_to_config, go_to_dashboard, course_id)],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ))
            page.update()

        lesson_content = ft.Column(
            [
                ft.TextButton(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.ARROW_BACK, size=16),
                            ft.Text("Volver al curso", size=12),
                        ],
                        spacing=4,
                    ),
                    on_click=return_to_course
                ),
                ft.Text(f"Estás en: {lesson_title}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Aquí irá la plantilla interactiva de la lección.", size=13, color=ft.Colors.GREY_500),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        )

        lesson_view = ft.View(
            route="/lesson",
            controls=[lesson_content],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.views.append(lesson_view)
        page.update()

    # Detectar si el modo oscuro está activo para adaptar los bloques dinámicamente
    is_dark = page.theme_mode == ft.ThemeMode.DARK

    # 2. Construir dinámicamente las lecciones basadas en el JSON
    lesson_controls = []
    for index, lesson in enumerate(lessons, start=1):
        lesson_name = lesson.get("title", f"Lección {index}")
        is_locked = lesson.get("locked", False)

        btn_text = "Bloqueado" if is_locked else "Iniciar"

        if is_locked:
            bg_color = ft.Colors.GREY_800 if is_dark else ft.Colors.GREY_100
            border_color = ft.Colors.GREY_700 if is_dark else ft.Colors.GREY_300
            btn_color = ft.Colors.GREY_700 if is_dark else ft.Colors.GREY_400
        else:
            bg_color = ft.Colors.GREY_900 if is_dark else ft.Colors.GREEN_50
            border_color = ft.Colors.GREEN_700 if is_dark else ft.Colors.GREEN_200
            btn_color = ft.Colors.GREEN_600

        lesson_row = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Unidad {index}", size=12, color=ft.Colors.GREEN_400 if is_dark else ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
                            ft.Text(lesson_name, size=15, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.FilledButton(
                        content=ft.Text(btn_text),
                        color=ft.Colors.WHITE,
                        bgcolor=btn_color,
                        disabled=is_locked,
                        on_click=lambda _, l_title=lesson_name: go_to_lesson(l_title),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=15,
            bgcolor=bg_color,
            border_radius=12,
            border=ft.Border.all(1, border_color) if hasattr(ft, "Border") else ft.border.all(1, border_color),
        )
        lesson_controls.append(lesson_row)

    lessons_list = ft.ListView(
        expand=True,
        spacing=15,
        padding=10,
        controls=lesson_controls
    )

    # 3. Estructura principal de la vista del curso
    return ft.Column(
        [
            ft.Row([back_button], alignment=ft.MainAxisAlignment.START),
            ft.Text(course_title, size=18, weight=ft.FontWeight.BOLD),
            ft.Text(course_description, size=13, color=ft.Colors.GREY_500),
            ft.Divider(height=5, thickness=1),
            lessons_list,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True,
    )
