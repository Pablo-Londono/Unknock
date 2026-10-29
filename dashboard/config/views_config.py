import flet as ft


def get_config_view(
        page: ft.Page, go_to_dashboard, on_logout, toggle_theme=None
):
    is_light = page.theme_mode == ft.ThemeMode.LIGHT

    # Switch para cambiar entre Modo Claro y Oscuro
    theme_switch = ft.Switch(
        label=(
            "Modo Oscuro"
            if not is_light
            else "Modo Claro"
        ),
        value=not is_light,
        on_change=lambda e: (
            toggle_theme(e.control.value) if toggle_theme else None
        ),
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Volver",
                        on_click=lambda _: go_to_dashboard(),
                    ),
                    ft.Text("Configuración", size=20, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            ft.Divider(height=20, thickness=1),
            ft.Text("Apariencia", size=14, weight=ft.FontWeight.W_500),
            theme_switch,
            ft.Divider(height=20, thickness=1),
            ft.Text("Opciones de Cuenta", size=14, color=ft.Colors.GREY_600),
            ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400),
                        ft.Text("Cerrar Sesión", color=ft.Colors.RED_400),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                on_click=lambda _: on_logout(),
                width=280,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        expand=True,
    )