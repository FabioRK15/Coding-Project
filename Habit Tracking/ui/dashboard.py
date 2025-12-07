import flet as ft
from datetime import date
from calendar import monthrange

def build_calendar_section(state):
    calendar_label = ft.Text("Calendar", size=25, weight=ft.FontWeight.BOLD)

    calendar_grid = ft.GridView(
        expand=True,
        runs_count=7,
        max_extent=100,
        spacing=5,
        run_spacing=5,
    )

    def build_calendar():
        calendar_grid.controls.clear()
        year = date.today().year
        month = date.today().month
        days = monthrange(year, month)[1]

        for d in range(1, days + 1):
            calendar_grid.controls.append(
                ft.Container(
                    content=ft.Text(str(d)),
                    bgcolor="#dddddd",
                    alignment=ft.alignment.center,
                    border_radius=8,
                )
            )

    build_calendar()

    return ft.Column(
        [
            calendar_label,
            calendar_grid,
        ]
    )


def build_tree_dashboard_section(state):
    dashboard_label = ft.Text("Habit Tree Dashboard", size=25, weight=ft.FontWeight.BOLD)

    display = ft.Column()

    def update_dashboard(e=None):
        display.controls.clear()
        for h in state["habits"]:
            icon = "🌸" if h.type == "good" else "🍄"
            display.controls.append(
                ft.Text(f"{icon} {h.name} — Streak {h.streak}")
            )
        state["page"].update()

    state["update_dashboard"] = update_dashboard

    return ft.Column(
        [
            dashboard_label,
            ft.ElevatedButton("Refresh Tree", on_click=update_dashboard),
            display
        ]
    )