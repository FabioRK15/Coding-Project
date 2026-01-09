import flet as ft
import data.database as db
from pages.habit_editor import HabitsView
from pages.dashboard import DashboardView
from pages.breathing import BreathingView

def main(page: ft.Page):
    db.init_db()
    page.title = "Self-management Toolkit"

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(DashboardView(page)) 
            
        elif page.route == "/habits":
            page.views.append(HabitsView(page))
            
        elif page.route == "/breathing":
            page.views.append(BreathingView(page))

        page.update()
        
    #back button
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)    

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/") 

if __name__ == "__main__":
    ft.app(target=main)