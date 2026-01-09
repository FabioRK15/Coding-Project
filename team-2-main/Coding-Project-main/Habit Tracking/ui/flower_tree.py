import flet as ft
import os

def build_flower_garden(state):
    page = state["page"]

    # Flower overlay MUSS feste Größe haben
    flower_overlay = ft.Stack(
        width=300,
        height=300,
    )

    field_container = ft.Container(
        width=300,
        height=300,
        content=flower_overlay,
        alignment=ft.alignment.top_left,
        border=ft.border.all(2, "#4CAF50"),
        border_radius=10,
        bgcolor="#E8F5E9",
    )

    # Status: max 5 Flowers
    if "flower_status" not in state:
        state["flower_status"] = [False] * 5

    # Bildpfad
    icon_path = os.path.join(os.path.dirname(__file__), "icon.jpg")

    # FIXE Positionen (wie mushroom_positions)
    flower_positions = [
        {"top": 40, "left": 40}, 
        {"top": 40, "left": 200}, 
        {"top": 200, "left": 40}, 
        {"top": 200, "left": 200}, 
        {"top": 120, "left": 120},
    ]

    def update_flowers():
        flower_overlay.controls.clear()

        for idx, active in enumerate(state["flower_status"]):
            if active:
                flower_overlay.controls.append(
                    ft.Container(
                        content=ft.Stack(
                            width=40,
                            height=40,
                            controls=[
                                ft.Container(
                                    width=14,
                                    height=14,
                                    bgcolor="#FFD54F",
                                    border_radius=7,
                                    left=13,
                                    top=13,
                                    alignment=ft.alignment.center,
                                ),
                                ft.Container(width=12, height=12, bgcolor="#F06292", border_radius=6, left=14, top=0),
                                ft.Container(width=12, height=12, bgcolor="#F06292", border_radius=6, left=28, top=14),
                                ft.Container(width=12, height=12, bgcolor="#F06292", border_radius=6, left=14, top=28),
                                ft.Container(width=12, height=12, bgcolor="#F06292", border_radius=6, left=0, top=14),
                            ],
                        ),
                        **flower_positions[idx],
                    )
                )

        page.update()

    state["update_flowers"] = update_flowers

    update_flowers()
    return field_container