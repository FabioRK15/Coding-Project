import flet as ft
import asyncio
import time

# --- Configuration & Data ---
breathing_techniques = {
    "Focus Breathing": { # Renamed from Box Breathing
        "description": "Focus & Calm",
        "steps": [
            ("Inhale", 4, 1.0), 
            ("Hold", 4, 1.0),
            ("Exhale", 4, 0.5),
            ("Hold", 4, 0.5)
        ]
    },
    "Relaxation Breathing": { # Renamed from 4-7-8 Relax
        "description": "Sleep & Anxiety",
        "steps": [
            ("Inhale", 4, 1.0),
            ("Hold", 7, 1.0),
            ("Exhale", 8, 0.5)
        ]
    }
}

async def main(page: ft.Page):
    # --- UI Setup ---
    page.title = "Mindfulness Dashboard"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a" 

    # --- Audio Setup ---
    # Switched to a reliable OGG file from Wikimedia Commons
    bell_sound = ft.Audio(
        src="https://upload.wikimedia.org/wikipedia/commons/2/2c/Singing_bowl_low.ogg",
        autoplay=False,
        volume=1.0 # Increased volume to max
    )
    page.overlay.append(bell_sound)

    state = {"cancel": False}

    # 1. Text Elements
    status_text = ft.Text(
        value="Ready to breathe?",
        size=32,
        weight=ft.FontWeight.W_300, 
        color="#e2e8f0",
        animate_opacity=500,
        text_align=ft.TextAlign.CENTER,
    )
    
    sub_text = ft.Text(
        value="Select a technique below",
        size=14,
        color="#94a3b8",
        animate_opacity=500,
        text_align=ft.TextAlign.CENTER,
    )

    timer_text = ft.Text(
        value="", 
        size=48, 
        weight=ft.FontWeight.BOLD, 
        color="#ffffff",
        animate_opacity=300, 
    )

    # 2. Main Visual Component
    breathing_circle = ft.Container(
        width=150,
        height=150,
        border_radius=150,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#22d3ee", "#3b82f6"], 
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=30,
            color="#1d4ed8", 
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.NORMAL,
        ),
        animate=ft.Animation(1000, "easeInOut"),
        alignment=ft.alignment.center,
        content=timer_text,
    )

    # Wrapper to prevent layout shifts when circle resizes
    circle_wrapper = ft.Container(
        content=breathing_circle,
        width=320, 
        height=320,
        alignment=ft.alignment.center,
    )

    # 3. Custom Input Fields
    def create_time_input(label):
        return ft.TextField(
            label=label,
            value="4",
            width=70,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(font_family="Roboto Mono", color="white"),
            border_color="#334155",
            focused_border_color="#3b82f6",
            text_size=14,
            height=50,
            content_padding=10
        )

    input_inhale = create_time_input("In")
    input_hold1 = create_time_input("Hold")
    input_exhale = create_time_input("Out")
    input_hold2 = create_time_input("Hold")

    custom_inputs_row = ft.Row(
        [input_inhale, input_hold1, input_exhale, input_hold2],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False, # Hidden by default
    )

    # 4. Logic Functions
    async def handle_dropdown_change(e):
        if method_dropdown.value == "Custom":
            custom_inputs_row.visible = True
            sub_text.value = "Customize your duration (seconds)"
        else:
            custom_inputs_row.visible = False
            sub_text.value = "Select a technique below"
        page.update()

    async def cancel_session(e):
        state["cancel"] = True
        cancel_btn.text = "Stopping..."
        cancel_btn.disabled = True
        page.update()

    async def run_exercise(e):
        state["cancel"] = False
        
        # Determine Steps
        technique_name = method_dropdown.value
        if technique_name == "Custom":
            try:
                i = int(input_inhale.value)
                h1 = int(input_hold1.value)
                e_val = int(input_exhale.value)
                h2 = int(input_hold2.value)
                steps = [
                    ("Inhale", i, 1.0),
                    ("Hold", h1, 1.0),
                    ("Exhale", e_val, 0.5),
                    ("Hold", h2, 0.5)
                ]
            except ValueError:
                status_text.value = "Please enter valid numbers"
                page.update()
                return
        else:
            exercise = breathing_techniques[technique_name]
            steps = exercise['steps']

        # Transition UI
        start_btn.visible = False
        method_dropdown.visible = False 
        custom_inputs_row.visible = False 
        
        cancel_btn.visible = True
        cancel_btn.text = "Cancel Session"
        cancel_btn.disabled = False
        
        status_text.value = technique_name if technique_name != "Custom" else "Custom Session"
        sub_text.value = "Relax and follow the circle..."
        timer_text.value = ""
        page.update()
        
        # Initial Buffer
        for _ in range(20): 
            if state["cancel"]: break
            await asyncio.sleep(0.1)

        # Breathing Loop
        if not state["cancel"]:
            for cycle in range(3):
                if state["cancel"]: break
                
                sub_text.value = f"Cycle {cycle + 1} of 3"
                page.update()
                
                await asyncio.sleep(0.5)

                for label, duration, scale in steps:
                    if state["cancel"]: break
                    
                    # Play Sound
                    try:
                        bell_sound.play()
                    except Exception:
                        print("Audio failed to play")

                    status_text.value = label
                    target_size = 300 * scale
                    
                    # Color Logic
                    if label == "Hold":
                        status_text.color = "#93c5fd" 
                        breathing_circle.gradient.colors = ["#60a5fa", "#3b82f6"]
                    elif label == "Exhale":
                        status_text.color = "#c4b5fd"
                        breathing_circle.gradient.colors = ["#22d3ee", "#3b82f6"]
                    else: # Inhale
                        status_text.color = "#6ee7b7"
                        breathing_circle.gradient.colors = ["#22d3ee", "#3b82f6"]

                    breathing_circle.width = target_size
                    breathing_circle.height = target_size
                    
                    breathing_circle.animate = ft.Animation(
                        duration * 1000,
                        "easeInOut" 
                    )
                    page.update()

                    # Precise Countdown Logic
                    start_time = time.time()
                    while (time.time() - start_time) < duration:
                        if state["cancel"]: break
                        
                        remaining = int(duration - (time.time() - start_time))
                        if remaining >= 0:
                            new_timer_value = str(remaining + 1)
                            if timer_text.value != new_timer_value:
                                timer_text.value = new_timer_value
                                page.update()
                        await asyncio.sleep(0.05)

                    timer_text.value = ""
                    page.update()

        # Reset UI
        if state["cancel"]:
            status_text.value = "Session Cancelled"
            sub_text.value = "Take a moment..."
        else:
            status_text.value = "Session Complete"
            sub_text.value = "Great job!"
        
        status_text.color = "#e2e8f0"
        
        breathing_circle.width = 150
        breathing_circle.height = 150
        breathing_circle.gradient.colors = ["#22d3ee", "#3b82f6"]
        breathing_circle.animate = ft.Animation(1000, "bounceOut")
        
        start_btn.visible = True
        method_dropdown.visible = True 
        cancel_btn.visible = False
        
        if method_dropdown.value == "Custom":
            custom_inputs_row.visible = True
        
        page.update()

    # 4. Controls & Layout
    options_list = [ft.dropdown.Option(k) for k in breathing_techniques.keys()]
    options_list.append(ft.dropdown.Option("Custom"))

    method_dropdown = ft.Dropdown(
        width=250,
        options=options_list,
        value="Focus Breathing", # Updated default
        label="Technique",
        border_color="#334155",
        color="#f1f5f9",
        bgcolor="#1e293b",
        focused_border_color="#3b82f6",
        text_size=16,
        on_change=handle_dropdown_change
    )

    start_btn = ft.ElevatedButton(
        text="Start Session",
        on_click=run_exercise,
        height=55,
        width=250,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor="#3b82f6", 
            color="#ffffff",
            elevation=2, 
        )
    )

    cancel_btn = ft.TextButton(
        text="Cancel Session",
        on_click=cancel_session,
        visible=False,
        style=ft.ButtonStyle(
            color="#9f1239", 
        )
    )

    page.add(
        ft.Column(
            [
                ft.Container(height=20),
                status_text,
                sub_text,
                ft.Container(height=20),
                circle_wrapper, 
                ft.Container(height=30),
                method_dropdown,
                ft.Container(height=10),
                custom_inputs_row, 
                ft.Container(height=10),
                start_btn,
                cancel_btn 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)