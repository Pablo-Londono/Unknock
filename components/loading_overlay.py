import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Usamos asposix para estandarizar las barras de la ruta en Windows/Linux/Mac
GIF_PATH = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "resources", "dih_fish.gif")).replace("\\", "/")

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
                        src=GIF_PATH,
                        width=80,
                        height=80,
                        fit="contain",
                        repeat=ft.ImageRepeat.NO_REPEAT,
                    ),
                    self.status_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            bgcolor=ft.Colors.with_opacity(0.35, ft.Colors.BLACK),
            alignment="center",
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