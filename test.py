import flet as ft


def main(page: ft.Page):
    page.title = "Camino de Aprendizaje - Estilo Duolingo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#EBF5EE"  # Tono verde suave de fondo tipo Duolingo
    page.window_width = 400
    page.window_height = 750

    # Función auxiliar para crear los botones circulares del camino
    def crear_boton_camino(
        icono, color_fondo, offset_x, texto_tooltip, on_click=None
    ):
        return ft.Container(
            content=ft.IconButton(
                icon=icono,
                icon_color="white",
                icon_size=32,
                tooltip=texto_tooltip,
                on_click=on_click,
            ),
            width=75,
            height=75,
            bgcolor=color_fondo,
            border_radius=37.5,
            alignment=ft.alignment.center,
            offset=ft.Offset(offset_x, 0),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.BLACK26,
                offset=ft.Offset(0, 4),
            ),
        )

    # Acciones para las lecciones de la Etapa 1
    def click_leccion_1(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("¡Iniciando Lección 1: Introducción al tema!")
        )
        page.snack_bar.open = True
        page.update()

    def click_leccion_2(e):
        page.snack_bar = ft.SnackBar(ft.Text("¡Iniciando Lección 2: Refuerzo!"))
        page.snack_bar.open = True
        page.update()

    def click_examen(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("¡Iniciando Examen de la Etapa!")
        )
        page.snack_bar.open = True
        page.update()

    # Barra superior tipo app
    header = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.BOLT, color=ft.colors.AMBER, size=24),
                        ft.Text(
                            "Etapa 1: Fuerzas",
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                            size=16,
                        ),
                    ]
                ),
                ft.Row(
                    [
                        ft.Icon(
                            ft.icons.LOCAL_FIRE_DEPARTMENT,
                            color=ft.colors.ORANGE,
                            size=24,
                        ),
                        ft.Text(
                            "3",
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                            size=16,
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#132F4C",
        padding=15,
        border_radius=10,
        margin=ft.margin.only(bottom=20),
    )

    # Elementos del camino serpenteante (alineados en zig-zag con offsets horizontales)
    caminos = ft.Column(
        [
            header,
            ft.Container(height=20),
            # Círculo 1: Estrella (Introducción)
            crear_boton_camino(
                ft.icons.STAR_ROUNDED,
                "#2B547E",
                -0.8,
                "Lección 1: Introducción",
                click_leccion_1,
            ),
            ft.Container(height=40),
            # Círculo 2: Engranajes (Refuerzo)
            crear_boton_camino(
                ft.icons.SETTINGS,
                "#2B547E",
                0.8,
                "Lección 2: Refuerzo",
                click_leccion_2,
            ),
            ft.Container(height=40),
            # Círculo 3: Trofeo (Examen basado en la silueta proporcionada)
            crear_boton_camino(
                ft.icons.EMERGENCY,  # Se usa de referencia o icono similar al trofeo estilizado
                "#2B547E",
                -0.2,
                "Lección 3: Examen",
                click_examen,
            ),
            ft.Container(height=40),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Contenedor principal que simula la pantalla de un celular
    app_container = ft.Container(
        content=caminos,
        width=380,
        height=680,
        bgcolor="#F4FBF7",
        padding=20,
        border_radius=20,
        border=ft.border.all(2, "#D0E1D4"),
    )

    page.add(app_container)


ft.run(main)