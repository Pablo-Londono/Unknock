import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(BASE_DIR, "user_sign", "photos")


def get_user_photo_path(user_id):
    if not user_id:
        return None

    for ext in [".png", ".jpg", ".jpeg"]:
        photo_path = os.path.join(PHOTOS_DIR, f"{user_id}{ext}")
        if os.path.exists(photo_path):
            return photo_path
    return None


def get_top_header(page: ft.Page, current_user, go_to_config):
    settings_button = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        icon_size=18,
        tooltip="Configuración",
        on_click=lambda _: go_to_config(),
    )

    user_id = current_user.get("id", "") if current_user else ""
    photo_path = get_user_photo_path(user_id)

    if photo_path:
        avatar_content = ft.CircleAvatar(
            foreground_image_src=photo_path,
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

    user_card = ft.Container(
        content=ft.Row(
            [
                avatar_content,
                ft.Text(
                    current_user.get("user", "Usuario") if current_user else "Usuario",
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

    user_header = ft.Row(
        [
            user_card,
            settings_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=user_header,
        padding=ft.Padding(left=0, top=35, right=0, bottom=0)
    )