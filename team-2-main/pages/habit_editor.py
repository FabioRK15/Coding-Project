import flet as ft
import data.database as db

def HabitsView(page: ft.Page):

    good_examples = ["Gym", "Meditation", "Drink Water", "Reading", "Walk in Nature"]
    bad_examples = ["Smoking", "Social Media", "Sugar/Sweets", "Procrastination", "Fast Food"]

    
    selected_habit_type = ft.Ref[ft.RadioGroup]()
    habit_dropdown = ft.Dropdown(label="Choose a common habit", width=300, disabled=True)
    
    custom_habit_input = ft.TextField(label="Or type your own...", width=300)
    
    good_habits_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    bad_habits_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    def refresh_habits():
        good_habits_col.controls.clear()
        bad_habits_col.controls.clear()

        for h in db.get_habits_and_icons("Good"):
            row = create_habit_row(h)
            good_habits_col.controls.append(row)

        for h in db.get_habits_and_icons("Bad"):
            row = create_habit_row(h)
            bad_habits_col.controls.append(row)
            
        page.update()

    def create_habit_row(habit_data):
        h_id = habit_data['id']
        h_name = habit_data['name']
        h_type = habit_data['habit_type']
        h_image = habit_data['file_name']
    
        row_bgcolor = "#F4F8F4" if h_type == "Good" else "#FDF5E6"
        
        return ft.Container(
            bgcolor=row_bgcolor,             
            border_radius=10,                
            padding=10,                      
            margin=ft.margin.only(bottom=8),
            content=ft.Row([
                ft.Row([
                    ft.Image(
                    src=f"{h_image}.png", 
                    width=24,
                    height=24,
                ),
                    ft.Text(h_name, size=16, weight="bold", color="#121212"),
                ]),
                
                ft.Row([
                    #edit button
                    ft.IconButton(
                        icon=ft.Icons.EDIT, 
                        icon_color="#121212",
                        tooltip="Edit Name",
                        on_click=lambda e: open_edit_dialog(h_id, h_name)
                    ),
                    #delete button
                    ft.IconButton(
                        icon=ft.Icons.DELETE, 
                        icon_color="#DC2626",
                        tooltip="Delete Habit",
                        on_click=lambda e: delete_habit(h_id)
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
          
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_200))
        )

    def add_habit(e):
        habit_type = selected_habit_type.current.value
        if not habit_type:
            page.snack_bar = ft.SnackBar(ft.Text("Please select 'Good' or 'Bad'."))
            page.snack_bar.open = True
            page.update()
            return

        name = custom_habit_input.value.strip() or habit_dropdown.value
        
        if name:
            db.add_habit(name, habit_type)
            custom_habit_input.value = ""
            habit_dropdown.value = None
            refresh_habits()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a name or choose an option."))
            page.snack_bar.open = True
            page.update()

    def delete_habit(habit_id):
        db.delete_habit(habit_id)
        refresh_habits()


    def on_type_change(e):
        val = selected_habit_type.current.value
        habit_dropdown.disabled = False
        if val == "Good":
            habit_dropdown.options = [ft.dropdown.Option(x) for x in good_examples]
        else:
            habit_dropdown.options = [ft.dropdown.Option(x) for x in bad_examples]
        habit_dropdown.value = None
        page.update()


    edit_field = ft.TextField(label="New Name")
    current_edit_id = None

    def save_edit(e):
        if current_edit_id and edit_field.value:
            db.update_habit_name(current_edit_id, edit_field.value)
            edit_dialog.open = False
            refresh_habits()
            page.update()

    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit Habit"),
        content=edit_field,
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: page.close_dialog()),
            ft.TextButton("Save", on_click=save_edit),
        ],
    )

    def open_edit_dialog(h_id, old_name):
        nonlocal current_edit_id
        current_edit_id = h_id
        edit_field.value = old_name
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()


    input_section = ft.Container(
        padding=20,
        bgcolor="#ffffff",
        border_radius=15,
        content=ft.Column([
            ft.Text("Add a New Habit", size=22, weight="bold", color="#121212"),
            ft.RadioGroup(
                ref=selected_habit_type,
                content=ft.Row([
                    ft.Radio(value="Good", label="Good Habit"),
                    ft.Radio(value="Bad", label="Bad Habit"),
                ]),
                on_change=on_type_change
            ),
            ft.Row(
                [
                habit_dropdown, 
                custom_habit_input, 
                ft.ElevatedButton(
                    "Add Habit",
                    on_click=add_habit,
                    style=ft.ButtonStyle(
                        bgcolor="#2D5016",
                        color="#FFFFFF",
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    )
                )
                ], 
                spacing=15),
        ])
    )

  
    split_view = ft.Row(
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        controls=[
            #good habits
            ft.Container(
                expand=1,
                padding=15,
                bgcolor="#ffffff",
                border_radius=15,
                content=ft.Column([
                    ft.Row([
                        ft.Text("Keep Growing", size=22, weight="bold", color="#121212")
                    ]),
                    ft.Row([
                        ft.Text("Build positive daily routines", size=16, weight="medium", color="#121212")
                    ]),
                    good_habits_col
                ])
            ),
            #bad habits
            ft.Container(
                expand=1,
                padding=15,
                bgcolor="#ffffff",
                border_radius=15,
                content=ft.Column([
                    ft.Row([
                        ft.Text("Release & Let go", size=22, weight="bold", color="#121212")
                    ]),
                    ft.Row([
                        ft.Text("Break free from these patterns", size=16, weight="medium", color="#121212")
                    ]),
                    bad_habits_col
                ])
            )
        ]
    )
    
    header_section = ft.Container(
        width = 850,  
         
        
        padding=ft.padding.only(left=20, top=20, bottom=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
    
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Edit your habits", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Customize your journey to better living", size=16, color=ft.Colors.GREY_700),
                    ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.START 
                ),
                ft.ElevatedButton(
                        text="Back to Dashboard",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda _: page.go("/"),
                        style=ft.ButtonStyle(
                            color="#FFFFFF",
                            bgcolor="#2D5016",
                            shape=ft.RoundedRectangleBorder(radius=6),
                        )
                ),
            ]
        )
    )
    
    
    def create_tip_col(title, text, add_separator=False):
        border = None
        if add_separator:
             border = ft.border.only(left=ft.border.BorderSide(1, ft.Colors.GREY_300))

        return ft.Container(
            expand=1,
            padding=ft.padding.symmetric(horizontal=20),
            border=border,
            content=ft.Column([
                ft.Text(title, weight="bold", color="#2D5016", size=16),
                ft.Text(text, size=14, color="#121212"),
            ], spacing=5)
        )


    tips_section = ft.Container(
        margin=ft.margin.only(top=20), 
        padding=25,
        bgcolor="#ffffff",
        border_radius=15,
        content=ft.Column([
            ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.LIGHTBULB, color="#2D5016", size=20),
                        padding=10, bgcolor=ft.Colors.GREEN_100, shape=ft.BoxShape.CIRCLE
                    ),
                    ft.Text("Tips for Success", size=20, weight="bold", color="#2D5016")
                ], spacing=15),
            
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                #color="#121212"
                controls=[
                    create_tip_col(
                        "Be specific", 
                        'Instead of "exercise more" try "20-minute morning walk"',
                        add_separator=False),
                    create_tip_col(
                        "Start small", 
                        "Focus on 3-5 key habits rather than overwhelming yourself", 
                        add_separator=True),
                    create_tip_col(
                        "Stay consistent", 
                        "Track daily to build momentum and see your progress", 
                        add_separator=True),
                ]
            )
        ])
    )


    refresh_habits()
    
    page_content = ft.Column(
        width=850,
        scroll=ft.ScrollMode.AUTO, 
        controls=[
            header_section,
            input_section,
            ft.Divider(height=20, color="transparent"),
            split_view,
            tips_section,
            ft.Divider(height=30, color="transparent"),
            #ft.ElevatedButton("Back to Dashboard", on_click=lambda _: page.go("/")),
        ]
    )
    
    '''
    page_content = ft.Column(
        width=850,  
        controls=[
            ft.AppBar(title=ft.Text("Manage Habits"), bgcolor=ft.colors.SURFACE_VARIANT),
            
            # Add some spacing from top
            ft.Divider(height=20, color="transparent"),
            header_section,
            
            # 1. Input Form
            input_section,
            
            ft.Divider(height=20, color="transparent"),
            
            # 2. Lists (Good/Bad)
            split_view,
            
            # 3. Tips Block
            tips_section,
            
            ft.Divider(height=30, color="transparent"),
            
            # 4. Back Button
            ft.ElevatedButton("Back to Dashboard", on_click=lambda _: page.go("/"))
        ]
    )
    '''


    return ft.View(
        route="/habits",
        bgcolor="#F5F1E8",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        
        
        
        
        controls=[
            page_content
        ]
    )
    '''
    return ft.View(
        route="/habits",
        bgcolor="#F5F1E8",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
        controls=[
            page_content
        ]
    )
    '''
    
    
    
    




if __name__ == "__main__":
    def test_main(page: ft.Page):
        db.init_db()
        def route_change(e):
            page.views.clear()
            page.views.append(HabitsView(page))
            page.update()
            
        page.on_route_change = route_change
        page.go("/habits")

    ft.app(target=test_main)
'''
if __name__ == "__main__":
    def test_main(page: ft.Page):
        page.title = "Habit Manager Test"
        page.scroll = ft.ScrollMode.AUTO
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.bgcolor = "#FAF9F6"
        
        
        view = HabitsView(page)
        page.add(*view.controls) 
        
    ft.app(target=test_main)
'''