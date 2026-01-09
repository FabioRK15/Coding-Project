from ui.create_habit import build_create_section
from ui.logging import build_logging_section
from ui.mushroom_tree import build_mushroom_tree  # NEW: Import mushroom tree
from ui.flower_tree import build_flower_garden
import flet as ft
import os


def main(page: ft.Page):
    page.title = "Habit Tracker"
    page.scroll = "auto"

    # zentraler Zustand
    state = {
        "page": page,
        "habits": [],
        "selected_date": None,
        "controls": {},
        "update_log_options": lambda: None,
        "refresh_habit_list": lambda: None,
        "update_streaks": lambda: None,
        "update_dashboard": lambda: None,
        "update_mushrooms": lambda: None,  # Mushroom update callback
        "update_flowers": lambda: None,  # Flower update callback
        "flower_status": [False]*5,      # Status für 5 Blumen
    }

    # kleine Streak-Anzeige
    streak_label = ft.Text("Streak Overview", size=20, weight=ft.FontWeight.BOLD)
    streak_list = ft.Column()

    def refresh_habit_list():
        pass  # logging module übernimmt listing
    state["refresh_habit_list"] = refresh_habit_list

    def update_streaks():
        streak_list.controls.clear()
        for h in state["habits"]:
            streak_list.controls.append(
                ft.Text(f"{h.name} ({h.type}) — Streak: {h.streak}")
            )
        page.update()
    state["update_streaks"] = update_streaks

    # ===== FUNCTIONS =====
    def add_flower_habit():
        for idx, active in enumerate(state["flower_status"]):
            if not active:
                state["flower_status"][idx] = True
                break
        # direkt das Flower Overlay aktualisieren
        if state.get("update_flowers"):
            state["update_flowers"]()

    # ===== VIEWS =====

    def home_view():
        return ft.View(
            route="/",
            controls=[
                ft.Text("Habit Tracking Dashboard", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.ElevatedButton("Create Habit", on_click=lambda _: page.go("/create")),
                ft.ElevatedButton("Daily Logging", on_click=lambda _: page.go("/log")),
                ft.ElevatedButton("Streak Overview", on_click=lambda _: page.go("/streaks")),
                ft.ElevatedButton("Habit Tree Dashboard", on_click=lambda _: page.go("/tree")),
                ft.ElevatedButton(  # Mushroom Garden button
                    "🍄 Mushroom Garden", 
                    on_click=lambda _: page.go("/mushrooms"),
                    bgcolor="#4CAF50",
                    color="white"
                ),
                ft.ElevatedButton(
                    "🌸 Flower Garden",
                    on_click=lambda _: page.go("/positives"),
                    bgcolor="#4CAF50",
                    color="white"
                ),
            ]
        )

    def create_view():
        create_section = build_create_section(state)
        return ft.View(
            route="/create",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                create_section
            ]
        )

    def logging_view():
        logging_section = build_logging_section(state)

        try:
            state["update_log_options"]()
        except Exception:
            pass

        try:
            state["refresh_habit_list"]()
            state["update_streaks"]()
        except Exception:
            pass

        try:
            if "update_mushrooms" in state and state["update_mushrooms"]:
                state["update_mushrooms"]()
        except Exception:
            pass

        try:
            if "update_flowers" in state and state["update_flowers"]:
                state["update_flowers"]()
        except Exception:
            pass

        return ft.View(
            route="/log",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                logging_section
            ]
        )

    def streak_view():
        return ft.View(
            route="/streaks",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                streak_label,
                streak_list
            ]
        )

    def mushroom_garden_view():
        mushroom_section = build_mushroom_tree(state)
        return ft.View(
            route="/mushrooms",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                ft.Text("🍄 Mushroom Garden", size=30, weight=ft.FontWeight.BOLD, color="#4CAF50"),
                ft.Divider(),
                mushroom_section,
                ft.Divider(),
                ft.Text("How it works:", size=18, weight=ft.FontWeight.BOLD),
                ft.Column([
                    ft.Text("• Each mushroom represents a bad habit", size=14),
                    ft.Text("• Mushrooms are red when the habit is active", size=14),
                    ft.Text("• Mushrooms turn gray when you avoid the habit for a day", size=14),
                    ft.Text("• Goal: Remove all 5 mushrooms!", size=14, weight=ft.FontWeight.BOLD, color="#4CAF50"),
                    ft.Text("• Maximum of 5 bad habits allowed", size=14, color="gray"),
                ], spacing=5),
                ft.ElevatedButton(
                    "Go to Daily Logging",
                    on_click=lambda _: page.go("/log"),
                    icon=ft.Icons.LOGIN,
                ),
            ],
            scroll="auto",
        )

    def positive_habit_view():
        flower_section = build_flower_garden(state)
        icon_path = os.path.join(os.path.dirname(__file__), "icon.jpg")
        icon_image = ft.Image(src=icon_path, width=100, height=100) if os.path.exists(icon_path) else None
        controls_list = [
            ft.ElevatedButton("\u2190 Back", on_click=lambda _: state["page"].go("/")),
            ft.Text("🌸 Flower Garden", size=30, weight=ft.FontWeight.BOLD, color="#4CAF50"),
            ft.Divider(),
            flower_section,
            ft.Divider(),
        ]
        if icon_image:
            controls_list.append(icon_image)
        controls_list.extend([
            ft.Text("How it works:", size=18, weight=ft.FontWeight.BOLD),
            ft.Column([
                ft.Text("• Each flower represents a good habit", size=14),
                ft.Text("• Flowers spawn when the habit is completed", size=14),
                ft.Text("• Maximum of 5 good habits allowed", size=14, color="gray"),
            ], spacing=5),
            ft.ElevatedButton(
                "Create New Good Habit",
                on_click=lambda _: page.go("/create"),
                icon=ft.Icons.ADD
            ),
            ft.ElevatedButton(
                "Go to Daily Logging",
                on_click=lambda _: state["page"].go("/log"),
                icon=ft.Icons.LOGIN,
            ),
        ])
        return ft.View(
            route="/positives",
            controls=controls_list,
            scroll="auto",
        )

    # ===== ROUTING =====

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_view())
        elif page.route == "/create":
            page.views.append(create_view())
        elif page.route == "/log":
            page.views.append(logging_view())
        elif page.route == "/streaks":
            page.views.append(streak_view())
        elif page.route == "/mushrooms":
            page.views.append(mushroom_garden_view())
        elif page.route == "/positives":
            page.views.append(positive_habit_view())
        else:
            page.views.append(home_view())

        page.update()

    page.on_route_change = route_change

    # initial load
    page.go("/")


ft.app(target=main)