import flet as ft
from datetime import date

def build_logging_section(state):
    page = state["page"]

    good_dropdown = ft.Dropdown(label="Select Good Habit", width=250)
    bad_dropdown = ft.Dropdown(label="Select Bad Habit", width=250)
    log_result = ft.Text("")

    def update_log_options():
        good_dropdown.options = [
            ft.dropdown.Option(h.name, h.name)
            for h in state["habits"]
            if h.type == "good"
        ]
        bad_dropdown.options = [
            ft.dropdown.Option(h.name, h.name)
            for h in state["habits"]
            if h.type == "bad"
        ]
        page.update()

    state["update_log_options"] = update_log_options

    def refresh_and_update():
        state["refresh_habit_list"]()
        state["update_streaks"]()
        page.update()

    # Good habit logging
    def log_good_done(e):
        selected = good_dropdown.value
        if not selected:
            return

        today = date.today()

        for h in state["habits"]:
            if h.name == selected and h.type == "good":
                if h.last_logged == today:
                    log_result.value = "Already logged today."
                else:
                    if h.last_logged and (today - h.last_logged).days == 1:
                        h.streak += 1
                    else:
                        h.streak = 1

                    h.last_logged = today
                    h.log_day(today, True)
                    log_result.value = f"{h.name} done! Streak: {h.streak}"
                break

        refresh_and_update()

    # Bad habit avoided
    def log_bad_avoided(e):
        selected = bad_dropdown.value
        if not selected:
            return

        today = date.today()

        for h in state["habits"]:
            if h.name == selected and h.type == "bad":
                if h.last_logged == today:
                    log_result.value = "Already logged today."
                else:
                    if h.last_logged and (today - h.last_logged).days == 1:
                        h.streak += 1
                    else:
                        h.streak = 1

                    h.last_logged = today
                    h.log_day(today, True)
                    log_result.value = f"{h.name} avoided! Streak: {h.streak}"
                break

        refresh_and_update()

    # Relapse for bad habits
    def log_relapse(e):
        selected = bad_dropdown.value
        if not selected:
            return

        today = date.today()

        for h in state["habits"]:
            if h.name == selected and h.type == "bad":
                h.streak = 0
                h.last_logged = today
                h.log_day(today, False)
                log_result.value = f"Relapse logged for {h.name}. Streak reset."

        refresh_and_update()

    state["controls"]["good_dropdown"] = good_dropdown
    state["controls"]["bad_dropdown"] = bad_dropdown

    return ft.Column(
        [
            ft.Text("Daily Logging", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Good Habits", size=18, weight=ft.FontWeight.BOLD),
            good_dropdown,
            ft.ElevatedButton("Good Habit Done", on_click=log_good_done),
            ft.Divider(),
            ft.Text("Bad Habits", size=18, weight=ft.FontWeight.BOLD),
            bad_dropdown,
            ft.Row(
                [
                    ft.ElevatedButton("Avoided", on_click=log_bad_avoided),
                    ft.ElevatedButton(
                        "Relapse",
                        on_click=log_relapse,
                        bgcolor="#ff3333",
                        color="white",
                    ),
                ]
            ),
            log_result,
        ]
    )