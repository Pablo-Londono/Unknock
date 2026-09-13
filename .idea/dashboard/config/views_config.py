import flet as ft


def get_config_view(
        page: ft.Page, go_to_dashboard, on_logout, on_theme_changed=None
):
    is_light = page.theme_mode == ft.ThemeMode.LIGHT

    theme_button = ft.ElevatedButton(
        content=ft.Text("Modo Claro (Azul)" if is_light else "Modo Oscuro (Verde)"),
        icon=ft.Icons.LIGHT_MODE if is_light else ft.Icons.DARK_MODE,
    )

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.DARK_MODE
            theme_button.content = ft.Text("Modo Oscuro")
            if on_theme_changed:
                on_theme_changed("dark")
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.LIGHT_MODE
            theme_button.content = ft.Text("Modo Claro")
            if on_theme_changed:
                on_theme_changed("light")
        page.update()

    theme_button.on_click = toggle_theme

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        tooltip="Volver",
        on_click=lambda _: go_to_dashboard(),
    )

    logout_button = ft.ElevatedButton(
        content=ft.Text("Cerrar Sesión"),
        icon=ft.Icons.LOGOUT,
        bgcolor=ft.Colors.RED_400,
        color=ft.Colors.WHITE,
        on_click=lambda _: on_logout(),
    )

    header = ft.Row(
        [
            back_button,
            ft.Text("Configuración", size=16, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    return ft.Column(
        [
            header,
            ft.Divider(height=10, thickness=1),
            ft.Text(
                "Ajustes de Apariencia", size=12, weight=ft.FontWeight.W_500
            ),
            theme_button,
            ft.Divider(height=20, thickness=1),
            logout_button,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        expand=True,
    )