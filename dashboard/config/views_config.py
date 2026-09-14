import flet as ft


def get_config_view(page: ft.Page, go_to_dashboard, on_logout, toggle_theme=None):
    """
    Vista de configuración que incluye la opción de cambiar el tema visual
    y cerrar sesión.
    """

    # Botón para regresar al Dashboard
    back_button = ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK, size=16),
                ft.Text("Volver al Dashboard", size=12),
            ],
            spacing=4,
        ),
        on_click=lambda _: go_to_dashboard(),
    )

    # Switch para alternar Modo Oscuro / Modo Claro
    theme_switch = ft.Switch(
        label="Modo Oscuro",
        value=page.theme_mode == ft.ThemeMode.DARK,
        on_change=lambda e: toggle_theme(e.control.value) if toggle_theme else None,
    )

    # Botón para cerrar sesión
    logout_button = ft.ElevatedButton(
        "Cerrar Sesión",
        icon=ft.Icons.LOGOUT,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        on_click=lambda _: on_logout(),
    )

    return ft.Column(
        [
            ft.Container(
                content=ft.Row([back_button], alignment=ft.MainAxisAlignment.START),
                padding=ft.Padding(top=35, left=0, right=0, bottom=0),
            ),
            ft.Divider(height=10, thickness=1),
            ft.Text("Configuración", size=18, weight=ft.FontWeight.BOLD),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Apariencia", size=14, weight=ft.FontWeight.W_500),
                            theme_switch,
                        ],
                        spacing=10,
                    ),
                    padding=15,
                )
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Cuenta", size=14, weight=ft.FontWeight.W_500),
                            logout_button,
                        ],
                        spacing=10,
                    ),
                    padding=15,
                )
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        expand=True,
    )