import flet as ft
import data.database as db
import sqlite3
from datetime import date

def DashboardView(page: ft.Page):

    primary_green = "#2D5016"
    accent_red = "#FF6B6B"
    dark_text = "#2D3436"
    medium_text = "#636E72"
    border_color = "#E0E0E0"
    card_bg = "#FFFFFF"
    
    #Mushroom positions
    mushroom_positions = [
        {"left": 60, "top": 370},   # Position 1 - Left side (was 420)
        {"left": 140, "top": 370},  # Position 2 - Left center (was 440)
        {"left": 220, "top": 370},  # Position 3 - Center (was 420)
        {"left": 300, "top": 370},  # Position 4 - Right center (was 440)
        {"left": 380, "top": 370},  # Position 5 - Right side (was 420)
    ]

    mushroom_container = ft.Stack(
        width=500,
        height=500,
    )

    # Flower positions (on the tree)
    flower_positions = [
        {"left": 220, "top": 260},
        {"left": 260, "top": 230},
        {"left": 300, "top": 260},
        {"left": 240, "top": 300},
        {"left": 280, "top": 300},
    ]

    flower_container = ft.Stack(
        width=500,
        height=500,
    )
    
    def update_mushrooms():
        """Update mushroom display based on bad habits"""
        print(f"DEBUG: Updating mushrooms display")
        mushroom_container.controls.clear()
        
        # Get only bad habits (max 5)
        bad_habits = db.get_bad_habits_with_mushrooms()
        bad_count = len(bad_habits)
        
        # If no bad habits, don't show anything
        if bad_count == 0:
            page.update()
            return
        
        # Show only first 5 bad habits (5 mushroom limit)
        for i, habit in enumerate(bad_habits):
            if i >= 5: 
                break
                
            position = mushroom_positions[i]
            
            #check mushroom active status
            mushroom_active = habit.get('mushroom_active', 1)
            
            #get the mushroom image file from habit data
            mushroom_image = habit.get('file_name', f'mushroom_{i+1}')
            
            if mushroom_active:
                mushroom = ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src=f"assets/{mushroom_image}.png",
                            width=40,
                            height=40,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        
                        ft.Container(
                            content=ft.Text(
                                f"#{i+1}",
                                size=10,
                                weight="bold",
                                color="black" 
                            ),
                            bgcolor="#FFFFFFA0", 
                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            border_radius=10,
                            border=ft.border.all(1, "#CCCCCC"),
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    **position,
                    tooltip=f"{habit['name']} (Active - Click checkbox to remove)",
                    data=habit['id'],
                )
            else:
                mushroom = ft.Container(
                    content=ft.Stack([
                        #graying out the mushroom image
                        ft.Image(
                            src=f"assets/{mushroom_image}.png",
                            width=40,
                            height=40,
                            fit=ft.ImageFit.CONTAIN,
                            color="#BDBDBD",
                            color_blend_mode=ft.BlendMode.MULTIPLY,
                            opacity=0.5,
                        ),
                        #green checkmark on mushroom 
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.CHECK_CIRCLE,
                                size=30,
                                color="green",
                            ),
                            alignment=ft.alignment.center,
                        ),
                    ], width=40, height=40),
                    **position,
                    tooltip=f"{habit['name']} ✓ Avoided today!",
                    data=habit['id'],
                )
            
            mushroom_container.controls.append(mushroom)
        
        
        page.update()
    
    def create_legend_item(habit_data):
        h_name = habit_data['name']
        h_image = habit_data['file_name']
        h_type = habit_data['habit_type']
        
        #showing mushroom for bad habits
        if h_type == "Bad":
            return ft.Container(
                content=ft.Row([
                    ft.Image(
                        src=f"assets/{h_image}.png",
                        width=24,
                        height=24
                    ),
                    ft.Text(
                        h_name, size=14, color=dark_text
                    )
                ], spacing=8)
            )
        else:
            #showing flower for good habits
            return ft.Container(
                content=ft.Row([
                    ft.Image(
                        src=f"assets/{h_image}.png",
                        width=24,
                        height=24
                    ),
                    ft.Text(
                        h_name, size=14, color=dark_text
                    )
                ], spacing=8)
            )
        
    habit_legend_container = ft.GridView(
        expand=True,
        runs_count=3,
        child_aspect_ratio=4,
        spacing=10,
        run_spacing=5,
    )

    def go_to_habits(e):
        page.go("/habits")

  
    good_habits_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    bad_habits_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    
    def create_dashboard_habit_row(habit_data):
        h_id = habit_data['id']
        h_name = habit_data['name']
        h_type = habit_data['habit_type']
        
        main_color = primary_green if h_type == "Good" else "#8E600B"
        
        def on_checkbox_change(e):
            print(f"{h_name} checked: {e.control.value}")
            
            #when the checkbox is checked for a bad habit it means it is avoided
            if h_type == "Bad" and e.control.value:
                #update mushroom status in database
                db.update_mushroom_status(h_id, False)
                
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"✓ Great! You avoided '{h_name}'. Mushroom removed!"),
                    bgcolor="#4CAF50"
                )
                page.snack_bar.open = True

                update_mushrooms()
                page.update()

                update_statistics()

            if h_type == "Good" and e.control.value:
                db.update_flower_status(h_id, True)

                page.snack_bar = ft.SnackBar(
                    ft.Text(f"🌸 Nice! '{h_name}' completed. Flower grown!"),
                    bgcolor="#4CAF50"
                )
                page.snack_bar.open = True

                update_flowers()
                page.update()
        
        #check if this bad habit mushroom is already removed
        is_checked = False
        if h_type == "Bad":
            mushroom_active = habit_data.get('mushroom_active', 1)
            is_checked = not mushroom_active 
        
        return ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=is_checked,  
                    scale=1.2, 
                    shape=ft.RoundedRectangleBorder(radius=4),
                    fill_color={
                        ft.ControlState.SELECTED: main_color,
                        ft.ControlState.HOVERED: main_color,
                        ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    },
                    check_color={
                        ft.ControlState.SELECTED: ft.Colors.WHITE,
                        ft.ControlState.HOVERED: ft.Colors.TRANSPARENT,
                    },
                    overlay_color=ft.Colors.TRANSPARENT,
                    on_change=on_checkbox_change
                ),

                ft.Text(
                    h_name,
                    size=16,
                    color=dark_text,
                    weight=ft.FontWeight.W_500
                ),
            ],
            alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(vertical=2)
        )
    
    def update_statistics():
        total_habits = len(db.get_habits_and_icons("Good")) + len(db.get_habits_and_icons("Bad"))
        active_mushrooms = db.get_active_mushroom_count()
        bad_habit_count = db.get_bad_habit_count()
        
        print(f"DEBUG: Total habits: {total_habits}, Active mushrooms: {active_mushrooms}, Bad habits: {bad_habit_count}")
        
        
    
    def refresh_dashboard_habits():
        good_habits_list.controls.clear()
        bad_habits_list.controls.clear()
        habit_legend_container.controls.clear()
        
        all_good = db.get_habits_and_icons("Good")
        all_bad = db.get_habits_and_icons("Bad")

        for h in all_good:
            good_habits_list.controls.append(create_dashboard_habit_row(h))
            habit_legend_container.controls.append(create_legend_item(h))

        #only show first 5 bad habits in the list (matching mushrooms)
        for h in all_bad[:5]:
            bad_habits_list.controls.append(create_dashboard_habit_row(h))
            habit_legend_container.controls.append(create_legend_item(h))
        
        update_mushrooms()
        update_flowers()
        update_statistics()
        page.update()

    def reset_mushrooms(e):
        db.reset_all_mushrooms()
        update_mushrooms()
        refresh_dashboard_habits()
        
        page.snack_bar = ft.SnackBar(
            ft.Text("✓ All mushrooms reset to active!"),
            bgcolor="#4CAF50"
        )
        page.snack_bar.open = True
        page.update()

    header_section = ft.Container(
        content=ft.Column([
            ft.Container(height=30),
            ft.Container(
                content=ft.Text("Self-management Toolkit", size=32, weight=ft.FontWeight.W_700, color=dark_text),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=8)
            ),
            ft.Container(
                content=ft.Text("Track habits, visualize growth, and guide your wellbeing", size=16, color=medium_text),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20)
            ),
            
        ])
    )

    breathing_list = ft.Column(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("Focus Breathing", size=15, color=dark_text)
            ], spacing=8),
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("Relaxation Breathing", size=15, color=dark_text)
            ], spacing=8),
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("Smooth Breathing", size=15, color=dark_text)
            ], spacing=8),
        ], spacing=12
    
    )
        
    

    breathing_card = ft.Container(
        content=ft.Column([
            ft.Text("Breathing Methods", size=20, weight="bold", color=primary_green),
            ft.Text("Check guided breathing techniques to reduce anxiety and enhance your well-being", size=14, color=medium_text),
            ft.Container(height=12),
            ft.Container(content=breathing_list, padding=ft.padding.only(bottom=30)),
            ft.TextButton(
                content=ft.Row(
                    [
                        ft.Text("Explore methods", size=16, color=primary_green),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=16, color=primary_green)
                    ], 
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                on_click=lambda _: page.go("/breathing"), 
                style=ft.ButtonStyle(
                    color=primary_green,
                    bgcolor=ft.Colors.TRANSPARENT,
                    shadow_color=ft.Colors.TRANSPARENT,
                    overlay_color={"": ft.Colors.with_opacity(0.1, primary_green)},
                    padding=ft.padding.only(left=5, right=5),
                    shape=ft.RoundedRectangleBorder(radius=8)
                )
            )
        ]),
        padding=24, bgcolor=card_bg, border=ft.border.all(1, border_color), border_radius=12, height=380
    )

    
    statistics_card = ft.Container(
        content=ft.Column([
            ft.Text("Statistics", size=20, weight="bold", color=primary_green),
            ft.Row([ft.Text("Total habits"), ft.Container(expand=True), 
                   ft.Text(f"{len(db.get_habits_and_icons('Good')) + len(db.get_habits_and_icons('Bad'))}", weight="bold")]),
            ft.Row([ft.Text("Current streak"), ft.Container(expand=True), ft.Text("7 days", weight="bold")]),
            ft.Row([ft.Text("🍄 Active mushrooms"), ft.Container(expand=True), 
                   ft.Text(f"{db.get_active_mushroom_count()}/5", 
                          weight="bold",
                          color="green" if db.get_active_mushroom_count() == 0 else "orange")]),
            # Two separate reset buttons: Flowers (top) and Mushrooms (bottom)
            ft.ElevatedButton(
                "🔄 Reset Flowers",
                on_click=lambda e: [db.reset_all_flowers(), refresh_dashboard_habits(), setattr(page, 'snack_bar', ft.SnackBar(ft.Text("🌸 All flowers reset!"), bgcolor="#4CAF50")), setattr(page.snack_bar, 'open', True), page.update()],
                style=ft.ButtonStyle(
                    bgcolor="#E8FFE8", 
                    color="#2D5016",
                    padding=ft.padding.symmetric(horizontal=10, vertical=8)
                )
            ),
            ft.Container(height=10),  # spacing between buttons
            ft.ElevatedButton(
                "🔄 Reset Mushrooms",
                on_click=lambda e: [db.reset_all_mushrooms(), refresh_dashboard_habits(), setattr(page, 'snack_bar', ft.SnackBar(ft.Text("🍄 All mushrooms reset!"), bgcolor="#4CAF50")), setattr(page.snack_bar, 'open', True), page.update()],
                style=ft.ButtonStyle(
                    bgcolor="#FFE8E8", 
                    color="#FF6B6B",
                    padding=ft.padding.symmetric(horizontal=10, vertical=8)
                )
            ),
        ]),
        padding=24, bgcolor=card_bg, border=ft.border.all(1, border_color), border_radius=12, height=340, margin=ft.margin.only(top=20)
    )

    
    nav_button_style = ft.ButtonStyle(
        color=primary_green,
        bgcolor="#E8F4FF",
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        shape=ft.RoundedRectangleBorder(radius=8),
        elevation=0
    )

    keep_growing_card = ft.Container(
        content=ft.Column([
            ft.Text("Keep Growing", size=20, weight="bold", color=primary_green),
            ft.Text("Build positive daily routines", size=14, color=medium_text),
            ft.Container(height=6),
            ft.Container(
                content=good_habits_list,
                height=180,
            ),
            ft.Container(expand=True),
            ft.ElevatedButton("+ Add habit", style=nav_button_style, on_click=go_to_habits)
        ]),
        padding=24, bgcolor=card_bg, border=ft.border.all(1, border_color), border_radius=12, height=360
    )

    release_card = ft.Container(
        content=ft.Column([
            ft.Text("Release & Let Go", size=20, weight="bold", color="#8E600B"),
            ft.Text("Break free from patterns", size=14, color=medium_text),
            ft.Container(height=6),
            ft.Container(
                content=bad_habits_list,
                height=180,
            ),
            ft.Container(expand=True),
            ft.ElevatedButton("+ Add habit", on_click=go_to_habits, 
                             style=ft.ButtonStyle(color=accent_red, bgcolor="#FFE8E8", shape=ft.RoundedRectangleBorder(radius=8)))
        ]),
        padding=24, bgcolor=card_bg, border=ft.border.all(1, border_color), border_radius=12, height=360, margin=ft.margin.only(top=20)
    )

    
    left_col = ft.Column([breathing_card, statistics_card], width=300)
    
    
    tree_center = ft.Container(
        width=580,
        height=740,
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        border_radius=12,
        padding=20,
        content=ft.Stack([
            ft.Column([
                ft.Container(
                    content=ft.Image(
                        src="tree_no_bg.png",
                        width=450,
                        height=450,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),

                ft.Container(
                    bgcolor="#F8F9FA",
                    padding=20,
                    border_radius=15,
                    height=200,
                    content=habit_legend_container
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),

            ft.Container(
                content=flower_container,
                alignment=ft.alignment.top_left,
                width=500,
                height=500,
                margin=ft.margin.only(top=50, left=40)
            ),

            ft.Container(
                content=mushroom_container,
                alignment=ft.alignment.top_left,
                width=500,
                height=500,
                margin=ft.margin.only(top=50, left=40)
            )
        ])
    )
    
    right_col = ft.Column([keep_growing_card, release_card], width=300)

    main_layout = ft.Container(
        content=ft.Row([left_col, tree_center, right_col], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
        padding=ft.padding.only(top=24, bottom=20)
    )


    def update_flowers():
        """Update flower display based on good habits"""
        flower_container.controls.clear()

        good_habits = db.get_good_habits_with_flowers()

        for i, habit in enumerate(good_habits):
            if i >= 5:
                break

            if habit.get("flower_active", 0) != 1:
                continue

            position = flower_positions[i]
            flower_image = habit.get("file_name")

            flower = ft.Container(
                content=ft.Image(
                    src=f"assets/{flower_image}.png",
                    width=40,
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                ),
                tooltip=f"{habit['name']} ✓ Completed",
                **position,
            )

            flower_container.controls.append(flower)

        page.update()

    refresh_dashboard_habits()

    return ft.View(
        route="/",
        bgcolor="#F5F1E8",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Column([
                header_section,
                main_layout
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )