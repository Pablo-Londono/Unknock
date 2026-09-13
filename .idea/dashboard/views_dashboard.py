import os
import flet as ft

# Ruta al directorio de fotos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(BASE_DIR, "user_sign", "photos")


def get_user_photo_path(user_id):
    """Busca si existe foto para el ID en formato .png o .jpg"""
    if not user_id:
        return None

    for ext in [".png", ".jpg", ".jpeg"]:
        photo_path = os.path.join(PHOTOS_DIR, f"{user_id}{ext}")
        if os.path.exists(photo_path):
            return photo_path
    return None


def get_dashboard_view(page: ft.Page, current_user, go_to_config):
    # Botón de configuración (tuerca)
    settings_button = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        icon_size=18,
        tooltip="Configuración",
        on_click=lambda _: go_to_config(),
    )

    # Comprobar si existe foto de perfil para el ID del usuario
    user_id = current_user.get("id", "")
    photo_path = get_user_photo_path(user_id)

    if photo_path:
        avatar_content = ft.CircleAvatar(
            foreground_image_src=photo_path,  # Propiedad corregida
            radius=14,
        )
    else:
        avatar_content = ft.CircleAvatar(
            content=ft.Icon(
                ft.Icons.PERSON, color=ft.Colors.GREY_400, size=18
            ),
            bgcolor=ft.Colors.WHITE,
            radius=14,
        )

    # Tarjeta con foto de perfil y nombre de usuario
    user_card = ft.Container(
        content=ft.Row(
            [
                avatar_content,
                ft.Text(
                    current_user.get("user", "Usuario"),
                    size=12,
                    weight=ft.FontWeight.NORMAL,
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=8, top=4, right=8, bottom=4),
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=6,
    )

    # Encabezado superior
    user_header = ft.Row(
        [
            user_card,
            settings_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Column(
        [
            user_header,
            ft.Divider(height=10, thickness=1),
            ft.Text("Tus cursos", size=14, weight=ft.FontWeight.BOLD),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        expand=True,
    )