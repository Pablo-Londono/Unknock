import flet as ft

class LoadingOverlay:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_text = ft.Text(
            "Connecting to server...",
            color=ft.Colors.WHITE,
            size=14,
            weight=ft.FontWeight.BOLD
        )

        self.overlay = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        src="resources/dih_fish.gif",
                        width=105,
                        height=105,
                        fit="contain",
                    ),
                    self.status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                width=380,  # Coincide con el ancho de la ventana para un centrado perfecto sin fallos
                expand=True,
            ),
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            visible=False,
            expand=True,
        )

        # Limpiamos overlays previos para evitar acumulación al cerrar/abrir sesión
        self.page.overlay[:] = [o for o in self.page.overlay if o != self.overlay]

        if self.overlay not in self.page.overlay:
            self.page.overlay.append(self.overlay)

    def show(self, message="Connecting to server..."):
        self.status_text.value = message
        self.overlay.visible = True
        try:
            self.page.update()
        except Exception:
            pass

    def hide(self):
        self.overlay.visible = False
        try:
            self.page.update()
        except Exception:
            pass