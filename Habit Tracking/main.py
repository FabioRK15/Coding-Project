from ui.create_habit import build_create_section
from ui.logging import build_logging_section
from ui.dashboard import build_calendar_section, build_tree_dashboard_section
import flet as ft


def main(page: ft.Page):
    page.title = "Habit Tracker"
    page.scroll = "auto"

    # zentraler Zustand
    state = {
        "page": page,
        "habits": [],
        "controls": {},
        "update_log_options": lambda: None,
        "refresh_habit_list": lambda: None,
        "update_streaks": lambda: None,
        "update_dashboard": lambda: None
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
                ft.ElevatedButton("Calendar", on_click=lambda _: page.go("/calendar")),
                ft.ElevatedButton("Habit Tree Dashboard", on_click=lambda _: page.go("/tree")),
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
        # build the section first (this registers state['update_log_options'])
        logging_section = build_logging_section(state)

        # now populate the dropdown options (and refresh lists)
        try:
            state["update_log_options"]()
        except Exception:
            pass

        # also refresh habit list + streaks so UI is consistent
        try:
            state["refresh_habit_list"]()
            state["update_streaks"]()
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

    def calendar_view():
        cal = build_calendar_section(state)
        return ft.View(
            route="/calendar",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                cal
            ]
        )

    def tree_view():
        tree = build_tree_dashboard_section(state)
        return ft.View(
            route="/tree",
            controls=[
                ft.ElevatedButton("\u2190 Back", on_click=lambda _: page.go("/")),
                tree
            ]
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
        elif page.route == "/calendar":
            page.views.append(calendar_view())
        elif page.route == "/tree":
            page.views.append(tree_view())
        else:
            page.views.append(home_view())

        page.update()

    page.on_route_change = route_change

    # initial load
    page.go("/")


ft.app(target=main)