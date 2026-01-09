import flet as ft
import threading

def build_create_section(state):
    page = state["page"]

    habit_name = ft.TextField(label="Habit Name", width=250)

    # Predefined picker with "Custom"
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
        
        # NEW: Check mushroom limit for bad habits
        mushroom_id = None
        if habit_type.value == "bad":
            # Count existing bad habits
            existing_bad_habits = [h for h in state["habits"] if h.type == "bad"]
            
            # Check if maximum reached (5 mushrooms max)
            if len(existing_bad_habits) >= 5:
                # Show error message
                error_msg = ft.Container(
                    content=ft.Column([
                        ft.icon(ft.Icons.WARNING, color="orange", size=30),
                        ft.Text(
                            "Maximum 5 bad habits allowed!",
                            weight=ft.FontWeight.BOLD,
                            size=16,
                        ),
                        ft.Text(
                            "You can only track 5 bad habits (5 mushrooms).",
                            size=12,
                            color="white",
                        ),
                        ft.Text(
                            "Remove or complete existing bad habits first.",
                            size=12,
                            color="white",
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor="#d32f2f",
                    padding=15,
                    border_radius=10,
                    width=350,
                    top=20,
                    right=20,
                )
                page.overlay.append(error_msg)
                page.update()
                
                def hide_error():
                    if error_msg in page.overlay:
                        page.overlay.remove(error_msg)
                        page.update()
                
                threading.Timer(5, hide_error).start()
                return
            
            # Assign next mushroom ID (1-5)
            mushroom_id = len(existing_bad_habits) + 1
        
        # Create habit
        new_habit = Habit(name_to_use, habit_type.value)
        
        
        # NEW: Set mushroom ID for bad habits
        if mushroom_id:
            new_habit.mushroom_id = mushroom_id
        
        state["habits"].append(new_habit)

        # Update all callbacks
        state["update_log_options"]()
        state["refresh_habit_list"]()
        state["update_streaks"]()
        
        # NEW: Update mushroom display if function exists
        if "update_mushrooms" in state and callable(state["update_mushrooms"]):
            try:
                state["update_mushrooms"]()
            except Exception:
                pass

        # NEW: Update flower display if function exists
        if "update_flowers" in state and callable(state["update_flowers"]):
            try:
                state["update_flowers"]()
            except Exception:
                pass

        # Success message with mushroom info
        if habit_type.value == "bad":
            mushroom_text = f" (Mushroom #{mushroom_id})"
            emoji = "🍄"
            color = "#4CAF50"
        else:
            mushroom_text = ""
            emoji = "✅"
            color = "#323232"
        
        msg = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, color="white"),
                    ft.Text(
                        f"{emoji} Habit Created!",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color="white",
                    ),
                ], spacing=10),
                ft.Text(
                    f"{new_habit.name}{mushroom_text}",
                    color="white",
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    f"Type: {new_habit.type.capitalize()} habit",
                    size=12,
                    color="white",
                ),
            ], spacing=5),
            bgcolor=color,
            padding=15,
            border_radius=10,
            width=350,
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

        # Reset form
        predefined_picker.value = "custom"
        habit_name.value = ""
        habit_name.disabled = False
        habit_type.value = None
        
        # Reset predefined options
        predefined_picker.options = [ft.dropdown.Option("custom", "Custom")]
        
        page.update()

    create_button = ft.ElevatedButton(
        "Create Habit",
        on_click=create_habit,
        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
    )

    state["controls"]["predefined_picker"] = predefined_picker
    state["controls"]["habit_name"] = habit_name
    state["controls"]["habit_type"] = habit_type

    return ft.Column(
        [
            ft.Text("Create Habit", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Create new habits to track. Bad habits will appear as mushrooms in the garden.", 
                   size=12, color="gray"),
            ft.Divider(),
            habit_type,
            predefined_picker,
            habit_name,
            ft.Container(height=10),
            create_button,
            ft.Divider(),
            ft.Column([
                ft.Text("About Mushrooms:", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("• Bad habits get mushroom IDs (1-5)", size=12),
                ft.Text("• Maximum 5 bad habits allowed", size=12),
                ft.Text("• View mushrooms in Mushroom Garden", size=12),
                ft.Text("• Mushrooms disappear when you avoid bad habits", size=12),
            ], spacing=5),
        ],
        spacing=15,
    )