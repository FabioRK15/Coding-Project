import flet as ft

def DashboardView(page: ft.Page):
    
  
    
    primary_blue = "#2D5016"      # Blue for headers
    accent_red = "#FF6B6B"        # Red for Release section
    radio_selected = "#2D5016"    # Blue for selected radio
    radio_unselected = "#E0E0E0"  # Light gray for unselected radio
    dark_text = "#2D3436"         # Dark gray text
    medium_text = "#636E72"       # Medium gray text
    border_color = "#E0E0E0"      # Border color
    card_bg = "#FFFFFF"           # White background
    checkbox_color = "#2D5016"    # Blue for checkboxes
    
    def go_to_habits(e):
        page.go("/habits")

    def go_to_breathing(e):
        page.go("/breathing")
    
   
    main_container = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=0),
        bgcolor="#FFFFFF"
    )
    
    #---------------------------
    
    header_section = ft.Container(
        content=ft.Column([
            ft.Container(height=30),  # Top spacing
            
            # Main title - Exact from design
            ft.Container(
                content=ft.Text(
                    "Self-management Toolkit",
                    size=32,
                    weight=ft.FontWeight.W_700,
                    color=dark_text,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=8)
            ),
            
            
            ft.Container(
                content=ft.Text(
                    "Track habits, visualize growth, and guide your wellbeing",
                    size=16,
                    color=medium_text,
                    text_align=ft.TextAlign.CENTER
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=30)
            ),
            
            
            ft.Divider(height=1, color=border_color, thickness=1)
        ]),
        padding=0
    )
    
    
    breathing_radio_group = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(
                value="4-7-8",
                label="4-7-8 Technique",
                fill_color=radio_selected
            ),
            ft.Radio(
                value="box",
                label="Box Breathing",
                fill_color=radio_selected
            ),
            ft.Radio(
                value="mindful",
                label="Mindful Breathing",
                fill_color=radio_selected
            ),
        ], spacing=12),
        value="4-7-8"  # Default selected
    )
    
    breathing_card = ft.Container(
        content=ft.Column([
          
            ft.Container(
                content=ft.Text(
                    "Breathing Methods",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=primary_blue
                ),
                padding=ft.padding.only(bottom=8)
            ),
            
            
            ft.Container(
                content=ft.Text(
                    "Check guided breathing techniques to reduce anxiety and enhance your well-being",
                    size=14,
                    color=medium_text,
                    text_align=ft.TextAlign.LEFT
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            
            ft.Container(
                content=breathing_radio_group,
                padding=ft.padding.only(bottom=20)
            ),
            
           
           
            
            
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("Explore methods", 
                               size=14,
                               weight=ft.FontWeight.W_500),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=18)
                    ], spacing=8),
                    style=ft.ButtonStyle(
                        color=primary_blue,
                        bgcolor=ft.Colors.TRANSPARENT,
                        side=ft.border.BorderSide(1, primary_blue),
                        padding=ft.padding.symmetric(horizontal=24, vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0
                    ),
                    on_click=lambda e: print(f"Selected: {breathing_radio_group.value}")
                ),
                padding=ft.padding.only(top=20)
            )
        ]),
        padding=ft.padding.all(24),
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        border_radius=12,
        height=380,  # Fixed height for alignment
        alignment=ft.alignment.top_center
    )
    
    
    statistics_card = ft.Container(
        content=ft.Column([
            # Title
            ft.Container(
                content=ft.Text(
                    "Statistics",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color=primary_blue
                ),
                padding=ft.padding.only(bottom=16)
            ),
            
            
            ft.Column([
                # Total habits
                ft.Container(
                    content=ft.Row([
                        ft.Text("Total habits", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_400),
                        ft.Container(expand=True),
                        ft.Text("15", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_600),
                    ]),
                    padding=ft.padding.symmetric(vertical=8)
                ),
                
                # Current streak
                ft.Container(
                    content=ft.Row([
                        ft.Text("Current streak", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_400),
                        ft.Container(expand=True),
                        ft.Text("7 days", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_600),
                    ]),
                    padding=ft.padding.symmetric(vertical=8)
                ),
                
                # Habits eliminated
                ft.Container(
                    content=ft.Row([
                        ft.Text("Habits eliminated", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_400),
                        ft.Container(expand=True),
                        ft.Text("1", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_600),
                    ]),
                    padding=ft.padding.symmetric(vertical=8)
                ),
                
                # Breathing sessions
                ft.Container(
                    content=ft.Row([
                        ft.Text("Breathing sessions", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_400),
                        ft.Container(expand=True),
                        ft.Text("2", 
                               size=16, 
                               color=dark_text,
                               weight=ft.FontWeight.W_600),
                    ]),
                    padding=ft.padding.symmetric(vertical=8)
                ),
            ]),
            
            # Spacer
            ft.Container(height=0),
            
         
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Row([
                        ft.Text("View Details", 
                               size=14,
                               weight=ft.FontWeight.W_500),
                        ft.Icon(ft.Icons.ARROW_FORWARD, size=18)
                    ], spacing=8),
                    style=ft.ButtonStyle(
                        color=primary_blue,
                        bgcolor=ft.Colors.TRANSPARENT,
                        #side=ft.border.BorderSide(1, primary_blue),
                        padding=ft.padding.symmetric(horizontal=24, vertical=14),
                        #shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0
                    ),
                    on_click=lambda e: print("View Details clicked")
                ),
                padding=ft.padding.only(top=10)
            )
        ]),
        padding=ft.padding.all(24),
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        border_radius=12,
        margin=ft.margin.only(top=20),
        height=340,  # Fixed height for alignment
        alignment=ft.alignment.top_center
    )
    
    
    
    # TREE SECTION
    try:
        tree_image_content = ft.Image(
            src="C:\\Users\\HP\\Desktop\\welbeing project\\src\\treee.jpg",
            fit=ft.ImageFit.CONTAIN,
            border_radius=12
        )
    except:
        tree_image_content = ft.Container(
            height=300,
            bgcolor="#F8F9FA",
            border_radius=12,
            alignment=ft.alignment.center,
            content=ft.Text("Tree Image\n(Placeholder)", 
                           color=medium_text,
                           text_align=ft.TextAlign.CENTER)
        )
    
    # TODAY'S PROGRESS Section
    today_progress_section = ft.Container(
        content=ft.Column([
            ft.Row([
                # Drink 2 liters of water - COMPLETED
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#E8F4FF",
                            alignment=ft.alignment.center,
                            content=ft.Icon(ft.Icons.CHECK, color=primary_blue, size=24)
                        ),
                        ft.Container(height=8),
                        ft.Text("Drink 2 liters\nof water", 
                               size=12, 
                               color=dark_text, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Completed", 
                               size=10, 
                               color="#4CAF50", 
                               weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=8,
                    width=80
                ),
                
                # Meditation - COMPLETED
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#E8F4FF",
                            alignment=ft.alignment.center,
                            content=ft.Icon(ft.Icons.CHECK, color=primary_blue, size=24)
                        ),
                        ft.Container(height=8),
                        ft.Text("Meditation", 
                               size=12, 
                               color=dark_text, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Completed", 
                               size=10, 
                               color="#4CAF50", 
                               weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=8,
                    width=80
                ),
                
                # Learn German - COMPLETED
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#E8F4FF",
                            alignment=ft.alignment.center,
                            content=ft.Icon(ft.Icons.CHECK, color=primary_blue, size=24)
                        ),
                        ft.Container(height=8),
                        ft.Text("Learn\nGerman", 
                               size=12, 
                               color=dark_text, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Completed", 
                               size=10, 
                               color="#4CAF50", 
                               weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=8,
                    width=80
                ),
                
                # Read 5 pages - PENDING
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#F5F5F5",
                            alignment=ft.alignment.center,
                            content=ft.Text("R", 
                                           size=16, 
                                           color=medium_text, 
                                           weight=ft.FontWeight.W_500)
                        ),
                        ft.Container(height=8),
                        ft.Text("Read 5\npages", 
                               size=12, 
                               color=dark_text, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Pending", 
                               size=10, 
                               color=medium_text, 
                               weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=8,
                    width=80
                ),
                
                # Workout - PENDING
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            bgcolor="#F5F5F5",
                            alignment=ft.alignment.center,
                            content=ft.Text("W", 
                                           size=16, 
                                           color=medium_text, 
                                           weight=ft.FontWeight.W_500)
                        ),
                        ft.Container(height=8),
                        ft.Text("Workout", 
                               size=12, 
                               color=dark_text, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Pending", 
                               size=10, 
                               color=medium_text, 
                               weight=ft.FontWeight.W_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    padding=8,
                    width=80
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=8)
        ]),
        padding=ft.padding.symmetric(horizontal=16, vertical=20),
        bgcolor=card_bg,
        border_radius=12,
        height=180
    )
    
    # TREE CONTAINER - Height calculated to match other columns
    tree_container = ft.Container(
        width=580,
        height=740,  # Same height as left and right columns
        content=ft.Column([
           
            ft.Container(
                height=540, 
                content=ft.Container(
                    content=tree_image_content,
                    alignment=ft.alignment.center,
                    expand=True
                ),
                border=ft.border.all(1, border_color),
                border_radius=12,
                clip_behavior=ft.ClipBehavior.HARD_EDGE
            ),
            
            # Today's Progress at the bottom
            ft.Container(
                content=today_progress_section,
                margin=ft.margin.only(top=20),
                border=ft.border.all(1, border_color),
                border_radius=12
            )
        ], spacing=0),
        margin=ft.margin.symmetric(horizontal=10)
    )
    
    # KEEP GROWING SECTION - Right column
    keep_growing_checkboxes = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=True,
                    fill_color=ft.Colors.WHITE,
                    check_color=checkbox_color,
                ),
                ft.Text("Drink 2 liters of Water", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    fill_color=ft.Colors.WHITE,
                    check_color=checkbox_color,
                ),
                ft.Text("Workout", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    fill_color=ft.Colors.WHITE,
                    check_color=checkbox_color,
                ),
                ft.Text("Read 5 pages", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=True,
                    fill_color=ft.Colors.WHITE,
                    check_color=checkbox_color,
                ),
                ft.Text("Meditation", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=True,
                    fill_color=ft.Colors.WHITE,
                    check_color=checkbox_color,
                ),
                ft.Text("Learn German", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
    ], spacing=0)
    
    keep_growing_card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Keep Growing", 
                    size=20, 
                    weight=ft.FontWeight.W_600, 
                    color=primary_blue
                ),
                padding=ft.padding.only(bottom=4)
            ),
            
            ft.Container(
                content=ft.Text(
                    "Build positive daily routines",
                    size=14,
                    color=medium_text
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            keep_growing_checkboxes,
            
            ft.Container(expand=True),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "+ Add habit",
                    style=ft.ButtonStyle(
                        color=primary_blue,
                        bgcolor="#E8F4FF",
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0
                    )
                ),
                padding=ft.padding.only(top=20)
            )
        ]),
        padding=ft.padding.all(24),
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        border_radius=12,
        height=360,  # Fixed height for alignment
        alignment=ft.alignment.top_center
    )
    
    # RELEASE & LET GO SECTION
    release_checkboxes = ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    fill_color=ft.Colors.WHITE,
                    check_color=accent_red,
                ),
                ft.Text("Excessive scrolling", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=False,
                    fill_color=ft.Colors.WHITE,
                    check_color=accent_red,
                ),
                ft.Text("Late night snacking", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
        
        ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=True,
                    fill_color=ft.Colors.WHITE,
                    check_color=accent_red,
                ),
                ft.Text("Procrastinating tasks", 
                       size=16, 
                       color=dark_text),
            ], spacing=12),
            padding=ft.padding.symmetric(vertical=6)
        ),
    ], spacing=0)
    
    release_card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Release & Let Go", 
                    size=20, 
                    weight=ft.FontWeight.W_600, 
                    color=accent_red
                ),
                padding=ft.padding.only(bottom=4)
            ),
            
            ft.Container(
                content=ft.Text(
                    "Break free from these patterns",
                    size=14,
                    color=medium_text
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            release_checkboxes,
            
            ft.Container(expand=True),
            
            ft.Container(
                content=ft.ElevatedButton(
                    "+ Add habit",
                    style=ft.ButtonStyle(
                        color=accent_red,
                        bgcolor="#FFE8E8",
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0
                    )
                ),
                padding=ft.padding.only(top=20)
            )
        ]),
        padding=ft.padding.all(24),
        bgcolor=card_bg,
        border=ft.border.all(1, border_color),
        border_radius=12,
        margin=ft.margin.only(top=20),
        height=360,  # Fixed height for alignment
        alignment=ft.alignment.top_center
    )
    
    # Right column total height: 360 + 360 + 20 = 740px
    
    # Left column container
    left_column_with_stats = ft.Column([
        breathing_card,
        statistics_card
    ], spacing=0)
    
    # Right column container
    right_column_with_release = ft.Column([
        keep_growing_card,
        release_card
    ], spacing=0)
    
    # MAIN LAYOUT with BOTTOM ALIGNMENT
    main_layout_section = ft.Container(
        content=ft.Row([
            ft.Container(
                content=left_column_with_stats,
                width=300,
                margin=ft.margin.only(right=20),
            ),
            
            ft.Container(
                content=tree_container,
            ),
            
            ft.Container(
                content=right_column_with_release,
                width=300,
                margin=ft.margin.only(left=20),
            ),
        ], 
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START  # All start at top
        ),
        padding=ft.padding.only(top=24, bottom=20)
    )
    
    # MAIN CONTENT
    main_content = ft.Column([
        header_section,
        main_layout_section
    ], spacing=0)
    
    # Set main container content
    main_container.content = main_content
    
  
    
    return ft.View(
        route="/",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO, # Enables vertical scrolling for the whole dashboard
        controls=[
            ft.Column([
                header_section,
                main_layout
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]
    )

