import flet as ft
from typing import List
import os

def build_mushroom_tree(state):
    """Build the mushroom tree visualization"""
    page = state["page"]
    
    # Get only bad habits
    bad_habits = [h for h in state["habits"] if h.type == "bad"]
    
    # Get the tree image path
    # Adjust the path based on where your main.py is located
    # Since main.py is in Habit Tracking/, and tree.jpg is in src/
    tree_image_path = "src/tree.jpg"  # Relative path from main.py location
    
    # Check if file exists
    if not os.path.exists(tree_image_path):
        # Try alternative path
        tree_image_path = "../src/tree.jpg"
    
    # Title
    title = ft.Text(
        "Mushroom Garden",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#2E7D32",
    )
    
    # Tree image container
    tree_container = ft.Container(
        width=500,
        height=400,
        content=ft.Image(
            src=tree_image_path,
            width=500,
            height=400,
            fit=ft.ImageFit.CONTAIN,
        ),
        alignment=ft.alignment.center,
        border=ft.border.all(2, "#4CAF50"),
        border_radius=10,
        padding=10,
        bgcolor="#F1F8E9",
    )
    
    # Mushroom container (will be overlayed on tree)
    mushroom_overlay = ft.Stack(
        width=500,
        height=400,
    )
    
    # Mushroom positions (relative to tree image)
    # Adjust these based on your actual tree image
    mushroom_positions = [
        {"top": 80, "left": 150},   # Mushroom 1
        {"top": 120, "left": 350},  # Mushroom 2
        {"top": 180, "left": 100},  # Mushroom 3
        {"top": 220, "left": 300},  # Mushroom 4
        {"top": 280, "left": 200},  # Mushroom 5
    ]
    
    # Function to update mushrooms
    def update_mushrooms():
        mushroom_overlay.controls.clear()
        
        for habit in bad_habits:
            if habit.mushroom_id and habit.mushroom_id <= 5:
                position = mushroom_positions[habit.mushroom_id - 1]
                
                # Create mushroom icon
                if habit.mushroom_active:
                    # Active mushroom (red)
                    mushroom = ft.Column(
                        [
                            # Mushroom cap
                            ft.Container(
                                width=30,
                                height=20,
                                bgcolor="#FF5252",  # Red
                                border_radius=ft.border_radius.only(
                                    top_left=15,
                                    top_right=15,
                                    bottom_left=3,
                                    bottom_right=3,
                                ),
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=5,
                                    color=ft.Colors.RED_900,
                                ),
                            ),
                            # Mushroom stem
                            ft.Container(
                                width=8,
                                height=25,
                                bgcolor="#FFCCBC",
                                margin=ft.margin.symmetric(horizontal=11),
                            ),
                            # Label
                            ft.Container(
                                content=ft.Text(
                                    f"#{habit.mushroom_id}",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                                bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
                                padding=ft.padding.symmetric(horizontal=5, vertical=2),
                                border_radius=5,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    )
                else:
                    # Removed mushroom (faded with checkmark)
                    mushroom = ft.Column(
                        [
                            # Mushroom cap (faded)
                            ft.Container(
                                width=30,
                                height=20,
                                bgcolor="#BDBDBD",
                                border_radius=ft.border_radius.only(
                                    top_left=15,
                                    top_right=15,
                                    bottom_left=3,
                                    bottom_right=3,
                                ),
                                opacity=0.3,
                            ),
                            # Mushroom stem (faded)
                            ft.Container(
                                width=8,
                                height=25,
                                bgcolor="#E0E0E0",
                                margin=ft.margin.symmetric(horizontal=11),
                                opacity=0.3,
                            ),
                            # Checkmark
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CHECK_CIRCLE,
                                    size=20,
                                    color="green",
                                ),
                                bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                                border_radius=20,
                                padding=2,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    )
                
                mushroom_container = ft.Container(
                    content=mushroom,
                    **position,
                    on_click=lambda e, h=habit: show_habit_details(h),
                    tooltip=f"{habit.name}\nStatus: {habit.get_mushroom_status()}",
                )
                
                mushroom_overlay.controls.append(mushroom_container)
        
        # Update the page
        page.update()
    
    # Store update function in state
    state["update_mushrooms"] = update_mushrooms
    
    # Combined tree with mushrooms
    tree_with_mushrooms = ft.Stack(
        [
            tree_container,
            ft.Container(
                content=mushroom_overlay,
                alignment=ft.alignment.top_left,
            )
        ]
    )
    
    # Helper function
    def show_habit_details(habit):
        """Show details when mushroom is clicked"""
        dialog = ft.AlertDialog(
            title=ft.Text(f"🍄 Mushroom #{habit.mushroom_id}"),
            content=ft.Column([
                ft.Text(f"Habit: {habit.name}", weight=ft.FontWeight.BOLD),
                ft.Text(f"Type: Bad habit"),
                ft.Text(f"Current Streak: {habit.streak} days", 
                       color="green" if habit.streak > 0 else "orange"),
                ft.Text(f"Mushroom Status: {habit.get_mushroom_status()}",
                       color="red" if habit.mushroom_active else "green"),
                ft.Text(f"Last Logged: {habit.last_logged}" if habit.last_logged else "Never logged"),
                ft.Divider(),
                ft.Text("Tip: Log 'Avoided' in Daily Logging to remove this mushroom!", 
                       size=12, color="gray", italic=True),
            ], tight=True, spacing=8),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog(dialog)),
                ft.TextButton(
                    "Go to Logging", 
                    on_click=lambda e: [close_dialog(dialog), page.go("/log")]
                ),
            ],
        )
        
        def close_dialog(d):
            page.dialog = None
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    # Initial update
    update_mushrooms()
    
    # Progress text
    active_count = sum(1 for h in bad_habits if h.mushroom_active)
    progress_text = ft.Text(
        f"Progress: {5 - active_count}/5 mushrooms removed",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#4CAF50" if active_count == 0 else "#2E7D32",
    )
    
    # Habit list
    habit_list = ft.Column(
        spacing=10,
        scroll="auto",
        height=200,
    )
    
    def update_habit_list():
        habit_list.controls.clear()
        
        if not bad_habits:
            habit_list.controls.append(
                ft.Text("No bad habits created yet.", italic=True, color="gray")
            )
        else:
            for habit in bad_habits:
                habit_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(habit.name),
                        subtitle=ft.Text(
                            f"Mushroom #{habit.mushroom_id} • {habit.get_mushroom_status()}"
                        ),
                        leading=ft.Icon(
                            ft.Icons.WARNING if habit.mushroom_active else ft.Icons.CHECK_CIRCLE,
                            color="red" if habit.mushroom_active else "green"
                        ),
                        trailing=ft.Text(f"Streak: {habit.streak}"),
                    )
                )
    
    update_habit_list()
    
    # Complete component
    return ft.Column([
        title,
        progress_text,
        ft.Divider(),
        ft.Row([
            tree_with_mushrooms,
            ft.VerticalDivider(width=20),
            ft.Container(
                content=ft.Column([
                    ft.Text("Your Bad Habits:", size=16, weight=ft.FontWeight.BOLD),
                    habit_list,
                    ft.ElevatedButton(
                        "Create New Bad Habit",
                        on_click=lambda e: page.go("/create"),
                        icon=ft.Icons.ADD,
                    ),
                ]),
                width=300,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Text(
            "🎯 Each mushroom represents a bad habit. They disappear when you successfully avoid the habit for a day.",
            size=14,
            color="#2E7D32",
            text_align=ft.TextAlign.CENTER,
        ),
    ], scroll="auto")