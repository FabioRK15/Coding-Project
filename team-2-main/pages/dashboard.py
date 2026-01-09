import flet as ft
import data.database as db

def DashboardView(page: ft.Page):

    primary_green = "#2D5016"
    accent_red = "#FF6B6B"
    dark_text = "#2D3436"
    medium_text = "#636E72"
    border_color = "#E0E0E0"
    card_bg = "#FFFFFF"
    
    def create_legend_item(habit_data):
        h_name = habit_data['name']
        h_image = habit_data['file_name']
        return ft.Container(
            content=ft.Row([
                ft.Image(
                    src=f"{h_image}.png",
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
        h_name = habit_data['name']
        h_type = habit_data['habit_type']
        
        main_color = primary_green if h_type == "Good" else "#8E600B"
        
        return ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    scale=1.2, 
                    shape=ft.RoundedRectangleBorder(radius=4),
                    #border_side=ft.BorderSide(1.5, main_color), 
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
                    on_change=lambda e: print(f"{h_name} checked: {e.control.value}")
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
        
    def refresh_dashboard_habits():
        good_habits_list.controls.clear()
        bad_habits_list.controls.clear()
        habit_legend_container.controls.clear()
        
        all_good = db.get_habits_and_icons("Good")
        all_bad = db.get_habits_and_icons("Bad")

        '''for h in db.get_habits_by_type("Good"):
            good_habits_list.controls.append(create_dashboard_habit_row(h))

        for h in db.get_habits_by_type("Bad"):
            bad_habits_list.controls.append(create_dashboard_habit_row(h))'''
        
        for h in all_good:
            good_habits_list.controls.append(create_dashboard_habit_row(h))
            habit_legend_container.controls.append(create_legend_item(h))

        for h in all_bad:
            bad_habits_list.controls.append(create_dashboard_habit_row(h))
            habit_legend_container.controls.append(create_legend_item(h))
        
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
                padding=ft.padding.only(bottom=30)
            ),
            
        ])
    )

    breathing_list = ft.Column(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("4-7-8 Technique", size=15, color=dark_text)
            ], spacing=8),
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("Box Breathing", size=15, color=dark_text)
            ], spacing=8),
            ft.Row([
                ft.Icon(ft.Icons.CIRCLE, size=8, color=primary_green),
                ft.Text("Mindful Breathing", size=15, color=dark_text)
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
            ft.Row([ft.Text("Total habits"), ft.Container(expand=True), ft.Text("15", weight="bold")]),
            ft.Row([ft.Text("Current streak"), ft.Container(expand=True), ft.Text("7 days", weight="bold")]),
            ft.Row([ft.Text("Current streak"), ft.Container(expand=True), ft.Text("7 days", weight="bold")]),
            ft.Row([ft.Text("Current streak"), ft.Container(expand=True), ft.Text("7 days", weight="bold")]),
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
        content=ft.Column([
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
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    right_col = ft.Column([keep_growing_card, release_card], width=300)

    main_layout = ft.Container(
        content=ft.Row([left_col, tree_center, right_col], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
        padding=ft.padding.only(top=24, bottom=20)
    )

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