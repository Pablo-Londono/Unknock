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
                        src="resources/dih_fish.jpeg",
                        width=60,
                        height=60,
                        fit="contain",
                    ),
                    self.status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=ft.Colors.BLACK_54,
            alignment="center",  # <--- Usamos string literal "center" para evitar errores de atributo
            visible=False,
            expand=True,
        )

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