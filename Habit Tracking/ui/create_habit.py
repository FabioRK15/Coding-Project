import flet as ft
import threading

def build_create_section(state):
    page = state["page"]

    habit_name = ft.TextField(label="Habit Name", width=250)

    # Predefined picker with “Custom”
    predefined_picker = ft.Dropdown(
        label="Choose a predefined habit",
        width=250,
        options=[ft.dropdown.Option("custom", "Custom")]
    )

    # Handles switching between selecting & typing
    def on_predefined_change(e):
        if predefined_picker.value != "custom":
            habit_name.disabled = True
            habit_name.value = ""
        else:
            habit_name.disabled = False
        page.update()

    predefined_picker.on_change = on_predefined_change

    from data.predefined import predefined_good, predefined_bad

    def update_predefined(e):
        if habit_type.value == "good":
            predefined_picker.options = [ft.dropdown.Option("custom", "Custom")] + [
                ft.dropdown.Option(x, x) for x in predefined_good
            ]
        elif habit_type.value == "bad":
            predefined_picker.options = [ft.dropdown.Option("custom", "Custom")] + [
                ft.dropdown.Option(x, x) for x in predefined_bad
            ]
        page.update()

    habit_type = ft.Dropdown(
        label="Type",
        width=250,
        on_change=update_predefined,
        options=[
            ft.dropdown.Option("good", "good"),
            ft.dropdown.Option("bad", "bad"),
        ],
    )

    def create_habit(e):
        # Name auswählen
        if predefined_picker.value != "custom":
            name_to_use = predefined_picker.value
        else:
            name_to_use = habit_name.value.strip()

        if not name_to_use or not habit_type.value:
            return

        from models.habit import Habit
        new_habit = Habit(name_to_use, habit_type.value)
        state["habits"].append(new_habit)

        state["update_log_options"]()
        state["refresh_habit_list"]()
        state["update_streaks"]()

        # Banner
        msg = ft.Container(
    content=ft.Text(
        f"{new_habit.name} created successfully!",
        color="white",
        max_lines=2,
        overflow=ft.TextOverflow.ELLIPSIS,
    ),
    bgcolor="#323232",
    padding=15,
    border_radius=10,
    width=320,
    top=20,
    right=20,
)
        page.overlay.append(msg)
        page.update()

        def hide_msg():
            if msg in page.overlay:
                page.overlay.remove(msg)
                page.update()

        threading.Timer(5, hide_msg).start()

        # Reset
        predefined_picker.value = "custom"
        habit_name.value = ""
        habit_name.disabled = False

        page.update()

    create_button = ft.ElevatedButton("Create Habit", on_click=create_habit)

    state["controls"]["predefined_picker"] = predefined_picker
    state["controls"]["habit_name"] = habit_name
    state["controls"]["habit_type"] = habit_type

    return ft.Column(
        [
            ft.Text("Create Habit", size=25, weight=ft.FontWeight.BOLD),
            habit_type,
            predefined_picker,
            habit_name,
            create_button,
        ]
    )